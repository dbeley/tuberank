from django.contrib.auth.models import User
from django.db.models import QuerySet, Sum
from django.shortcuts import get_object_or_404, redirect
from rest_framework.exceptions import PermissionDenied
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext as _

from ratings import enums
from ratings.models.lists import VideoList, VideoListItem
from ratings.models.tags import UserTag, UserTagVote
from ratings.models.videos import Video, VideoRating, VideoViewing
from ratings.tags.serializers import UserTagSerializer
from ratings.videos.serializers import VideoRatingSerializer


def _add_video_to_list(video_pk: int, list_pk: int) -> bool:
    video_list = VideoList.objects.get(pk=list_pk)
    video = Video.objects.get(pk=video_pk)
    if video not in video_list.videos.all():
        first_available_rank = 1
        if video_list.items.exists():
            ranks = list(video_list.items.values_list("rank", flat=True))
            first_available_rank = min(set(range(1, max(ranks) + 2)) - set(ranks))
        VideoListItem.objects.create(
            list=video_list, video=video, rank=first_available_rank, description=""
        )
        return True
    return False


def _get_user_lists(user: User) -> QuerySet[VideoList]:
    return VideoList.objects.filter(user=user)


def _get_user_rating_for_video(user: User, video: Video) -> VideoRating | None:
    if VideoRating.objects.filter(
        video=video,
        user=user,
    ).exists():
        return VideoRating.objects.get(video=video, user=user)
    return None


def _get_tags_with_score_for_video(video: Video) -> list[dict]:
    result = []
    # Tag where total score is positive for specific video
    for tag in video.tags.all():
        score = tag.votes.filter(video=video).aggregate(score=Sum("vote"))["score"]
        if score and score > 0:
            result.append({"id": tag.pk, "name": tag.name, "score": score})
    return result


def _add_video_to_tag(tag_name: str, video: Video, user: User) -> None:
    tag, _ = UserTag.objects.get_or_create(
        name=tag_name,
        defaults={
            "user": user,
            "state": enums.TagState.VALIDATED,
        },
    )
    video.tags.add(tag)
    _add_vote_to_tag_video(tag, video, user, enums.TagVote.UPVOTE)


def _add_vote_to_tag_video(
    tag: UserTag, video: Video, user: User, vote: enums.TagVote
) -> None:
    if UserTagVote.objects.filter(video=video, user=user, tag=tag).exists():
        existing_vote = UserTagVote.objects.get(video=video, user=user, tag=tag)
        if vote != existing_vote.vote:
            existing_vote.delete()
    vote, _ = UserTagVote.objects.get_or_create(
        video=video, user=user, tag=tag, vote=vote
    )


def _get_related_videos(
    current_video: Video, tags_with_score: dict[str, str], count: int
) -> set[Video]:
    sorted_tags = sorted(tags_with_score, key=lambda d: d["score"], reverse=True)
    related_videos = set()
    # similarity by tag
    for tag in sorted_tags:
        if len(related_videos) >= count:
            break
        related_videos.update(
            UserTag.objects.get(pk=tag.get("id")).video_set.exclude(
                id=current_video.id
            )[: count - len(related_videos)]
        )
    # similarity by channel
    remaining = count - len(related_videos)
    if remaining > 0:
        related_videos.update(
            Video.objects.exclude(pk=current_video.pk)
            .filter(channel=current_video.channel)
            .all()[:remaining]
        )
    return related_videos


class VideoRatingDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "videos/video_rating.html"

    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        video_rating = _get_user_rating_for_video(user=request.user, video=video)
        if not video_rating:
            video_rating = VideoRating(video=video, user=request.user)
        serializer = VideoRatingSerializer(video_rating)
        return Response({"serializer": serializer, "video": video})

    def post(self, request, pk):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        video = get_object_or_404(Video, pk=pk)
        video_rating = VideoRating(video=video, user=request.user)
        serializer = VideoRatingSerializer(video_rating, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "video": video})
        VideoRating.objects.update_or_create(
            video=video,
            user=request.user,
            defaults={
                **serializer.validated_data,
            },
        )
        return redirect("video_details", pk=video.id)


class VideoViewingView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "videos/video_viewing.html"

    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        return Response({"video": video})

    def post(self, request, pk):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        video = get_object_or_404(Video, pk=pk)
        VideoViewing.objects.create(
            user=request.user,
            video=video,
            state=enums.ViewingState.VIEWED,
        )
        return redirect("video_details", pk=video.id)


class VideoDetailsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "videos/video_details.html"

    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        user_lists = None
        if request.user.is_authenticated:
            user_lists = _get_user_lists(request.user)
        lists = VideoList.objects.filter(videos__in=[pk])
        tags_with_score = _get_tags_with_score_for_video(video=video)
        related_videos = _get_related_videos(
            current_video=video, tags_with_score=tags_with_score, count=8
        )
        return Response(
            {
                "video": video,
                "user_lists": user_lists,
                "lists": lists,
                "tags": tags_with_score,
                "related_videos": related_videos,
            }
        )

    def post(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        user_lists = None
        notification = None
        if request.user.is_authenticated:
            user_lists = _get_user_lists(request.user)
            if "list_pk" in request.data:
                success = _add_video_to_list(
                    video_pk=video.pk, list_pk=request.data.get("list_pk")
                )
                if success:
                    notification = {
                        "title": "test",
                        "message": _("The video was successfully added to the list"),
                    }
            if "name" in request.data:
                serializer = UserTagSerializer(data=request.data)
                if not serializer.is_valid():
                    return Response({"video": video, "user_lists": user_lists})
                _add_video_to_tag(
                    tag_name=serializer.data.get("name"), video=video, user=request.user
                )
        lists = VideoList.objects.filter(videos__in=[pk])
        tags_with_score = _get_tags_with_score_for_video(video=video)
        related_videos = _get_related_videos(
            current_video=video, tags_with_score=tags_with_score, count=8
        )
        return Response(
            {
                "video": video,
                "user_lists": user_lists,
                "lists": lists,
                "notification": notification,
                "tags": tags_with_score,
                "related_videos": related_videos,
            }
        )


class VideoTagUpvoteView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "videos/video_details_tag_list.html"

    def post(self, request, video_id, tag_id):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        video = get_object_or_404(Video, pk=video_id)
        tag = get_object_or_404(UserTag, pk=tag_id, state=enums.TagState.VALIDATED)

        _add_vote_to_tag_video(tag, video, request.user, enums.TagVote.UPVOTE)

        score = tag.votes.filter(video=video).aggregate(score=Sum("vote"))["score"] or 0
        tag = {"id": tag.pk, "name": tag.name, "score": score}
        return Response(
            {
                "video": video,
                "tag": tag,
            }
        )


class VideoTagDownvoteView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "videos/video_details_tag_list.html"

    def post(self, request, video_id, tag_id):
        if not request.user.is_authenticated:
            raise PermissionDenied()
        video = get_object_or_404(Video, pk=video_id)
        tag = get_object_or_404(UserTag, pk=tag_id, state=enums.TagState.VALIDATED)

        _add_vote_to_tag_video(tag, video, request.user, enums.TagVote.DOWNVOTE)

        score = tag.votes.filter(video=video).aggregate(score=Sum("vote"))["score"] or 0
        if score == 0:
            video.tags.remove(tag)
        tag = {"id": tag.pk, "name": tag.name, "score": score}
        return Response(
            {
                "video": video,
                "tag": tag,
            }
        )
