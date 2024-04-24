from django.contrib.auth.models import User
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.users.serializers import UserSerializer


class UserListView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "users/user_list.html"

    def get(self, request):
        users = User.objects.filter(username__isnull=False, is_superuser=False)
        return Response({"users": UserSerializer(users, many=True).data})
