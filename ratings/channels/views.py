from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.models.videos import Video
from ratings.models.channels import Channel


class ChannelDetailsView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "channels/channel_details.html"

    def get(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)
        videos = Video.objects.filter(channel=channel)
        paginator = Paginator(videos, 8)
        page = paginator.get_page(request.GET.get("page", 1))
        return Response(
            {
                "channel": channel,
                "videos": page,
                "page": page,
            }
        )


class ChannelListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "channels/channel_list.html"

    def get(self, request):
        channels = Channel.objects.all()
        paginator = Paginator(channels, 12)
        page = paginator.get_page(request.GET.get("page", 1))
        return Response(
            {
                "channels": page,
            }
        )
