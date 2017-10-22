# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/10/22 15:10'

from rest_framework import serializers
from goods.models import Goods
from .models import ShoppingCart
from goods.serializers import GoodsSerializer


class ShopCartDetailSerializer(serializers.ModelSerializer):

    goods = GoodsSerializer(many=False)

    class Meta:
        model = ShoppingCart
        fields = "__all__"



class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1, error_messages={
        "min_value": "商品数量不能小于1",
        "required": "请选择购买数量"
    })
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), required=True)
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        # 查询数据库是否存在记录
        existed = ShoppingCart.objects.filter(user=user, goods=goods)

        if existed:
            # 如果存在，数量加1
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            # 如果不存在，创建新记录
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        # 修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance