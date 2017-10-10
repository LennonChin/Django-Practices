# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/10/10 21:58'

import django_filters
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    price_min = django_filters.NumberFilter(name='shop_price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(name='shop_price', lookup_expr='lte')

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max']

