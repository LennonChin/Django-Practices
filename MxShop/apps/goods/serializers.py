# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'

from rest_framework import serializers
from goods.models import Goods, GoodsCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Goods
        fields = "__all__" #('name', 'click_num', 'market_price', 'add_time', 'goods_front_image', 'goods_desc')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Goods.objects.create(**validated_data)
