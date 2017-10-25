from .serializers import GoodsSerializer, CategorySerializer
from rest_framework import mixins
from rest_framework import generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from .models import Goods, GoodsCategory, Banner
from .filter import GoodsFilter
from .serializers import BannerSerializer
# Create your views here.


class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100


class GoodsListView(generics.ListAPIView):
    """
    商品列表页
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination


class GoodsListViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    List:
        商品列表页
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    # 使用JWT不能开启这个Token方式的认证
    # authentication_classes = (TokenAuthentication, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')


class CategoryViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("-index")
    serializer_class = BannerSerializer

