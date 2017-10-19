from django.shortcuts import render
from rest_framework import mixins, viewsets
from .models import UserFav
from .serializers import UserFavSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

# Create your views here.


class UserFavViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    用户收藏功能
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
