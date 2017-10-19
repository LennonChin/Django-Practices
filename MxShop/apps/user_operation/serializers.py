# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/10/19 21:25'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import UserFav


class UserFavSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav

        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]

        fields = ("user", "goods", "id")