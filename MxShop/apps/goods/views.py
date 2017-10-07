from .serializers import GoodsSerializer
from rest_framework import mixins
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Goods
# Create your views here.


class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class GoodsListView(generics.ListAPIView):
    """
    商品列表页
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination