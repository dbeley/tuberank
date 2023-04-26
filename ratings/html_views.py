from ratings.models import Channel, ChannelRating, Video, VideoRating
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ratings.serializers import ChannelSerializer, ChannelRatingSerializer
from datetime import datetime, timezone
from django.shortcuts import redirect


class ChannelList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "channel_list.html"

    def get(self, request):
        queryset = Channel.objects.all()
        channels = ChannelSerializer(queryset, many=True)
        return Response({"channels": channels.data[:]})


class ChannelRatingDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "channel_rating_detail.html"

    def get(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        serializer = ChannelRatingSerializer(channel)
        return Response({"serializer": serializer, "channel": channel})

    def post(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        serializer = ChannelRatingSerializer(channel, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "channel": channel})
        serializer.save(
            user=self.request.user, date_publication=datetime.now(timezone.utc)
        )
        return redirect("channel_html")
