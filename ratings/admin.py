from django.contrib import admin
from ratings.models.videos import Video, VideoSnapshot, VideoRating
from ratings.models.channels import Channel, ChannelSnapshot, ChannelRating

admin.site.register(Channel)
admin.site.register(ChannelRating)
admin.site.register(ChannelSnapshot)
admin.site.register(Video)
admin.site.register(VideoRating)
admin.site.register(VideoSnapshot)
