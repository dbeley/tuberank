from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from ratings import views

router = routers.DefaultRouter()
router.register(r"channels", views.ChannelViewSet, basename="channels")
urlpatterns = router.urls
