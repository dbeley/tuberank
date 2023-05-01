from django.contrib import admin

from ratings.models.channels import Channel, ChannelRating, ChannelSnapshot
from ratings.models.videos import Video, VideoRating, VideoSnapshot

admin.site.register(Channel)
admin.site.register(ChannelRating)
admin.site.register(ChannelSnapshot)
admin.site.register(Video)
admin.site.register(VideoRating)
admin.site.register(VideoSnapshot)
