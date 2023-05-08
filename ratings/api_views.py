import http

from django.shortcuts import get_object_or_404
from rest_framework import views, authentication, throttling
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

import ratings.yt_import
from ratings import enums
from ratings.models import Video, VideoViewing


class ImportVideoView(views.APIView):
    authentication_classes = [
        authentication.SessionAuthentication,
        authentication.BasicAuthentication,
    ]
    throttle_classes = [throttling.UserRateThrottle, throttling.AnonRateThrottle]

    def post(self, request, yt_id):
        if not len(yt_id) == 11:
            raise ValidationError("YouTube id is most likely malformed")
        ratings.yt_import.create_video_snapshot(yt_id)
        if request.user.is_authenticated:
            video = get_object_or_404(Video, yt_id=yt_id)
            VideoViewing.objects.create(
                video=video, user=request.user, state=enums.ViewingState.VIEWED
            )
        return Response(status=http.HTTPStatus.OK)
