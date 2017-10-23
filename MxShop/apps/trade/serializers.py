# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/10/22 15:10'

import time

from rest_framework import serializers
from goods.models import Goods
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer
from utils.alipay import AliPay
from MxShop.const import private_key_path, alipay_key_path

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


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):

    goods = OrderGoodsSerializer(many=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, serializer):
        alipay = AliPay(
            appid="2016080600180695",
            app_notify_url="http://projectsedus.com/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=alipay_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.92.87.172:8000/alipay/return"
        )

        url = alipay.direct_pay(
            subject=serializer.order_sn,
            out_trade_no=serializer.order_sn,
            total_amount=serializer.order_amount
        )

        result_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return result_url

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_status = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    alipay_url = serializers.SerializerMethodField(read_only=True)

    def get_alipay_url(self, serializer):

        alipay = AliPay(
            appid="2016080600180695",
            app_notify_url="http://projectsedus.com/",
            app_private_key_path=private_key_path,
            alipay_public_key_path=alipay_key_path,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            debug=True,  # 默认False,
            return_url="http://47.92.87.172:8000/alipay/return"
        )

        url = alipay.direct_pay(
            subject=serializer.order_sn,
            out_trade_no=serializer.order_sn,
            total_amount=serializer.order_amount
        )

        result_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

        return result_url

    def generate_order_sn(self):
        # 当前时间 + user.id + 随机数
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{random_str}".format(time_str=time.strftime("%Y%m%d%H%M%S"),
                                                           userid=self.context["request"].user.id,
                                                           random_str=random_ins.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
