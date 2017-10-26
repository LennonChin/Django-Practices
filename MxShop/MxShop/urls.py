"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
import xadmin
from MxShop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from goods.views import GoodsListView, GoodsListViewset, CategoryViewset, BannerViewset, IndexCategoryViewset
from users.views import SmsCodeViewset, UserViewset
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from trade.views import ShopCartViewset, OrderViewset, AliPayView

from rest_framework_jwt.views import obtain_jwt_token

router = DefaultRouter()
router.register(r'goods', GoodsListViewset, base_name="goods")
router.register(r'categorys', CategoryViewset, base_name="category")
router.register(r'codes', SmsCodeViewset, base_name="codes")
router.register(r'users', UserViewset, base_name="users")

# 收藏
router.register(r'userfavs', UserFavViewset, base_name="userfavs")

router.register(r'messages', LeavingMessageViewset, base_name="messages")

router.register(r'address', AddressViewset, base_name="address")

router.register(r'shopcarts', ShopCartViewset, base_name="shopcarts")

# 訂單相關
router.register(r'orders', OrderViewset, base_name="orders")

# 轮播图
router.register(r'banners', BannerViewset, base_name="banners")

# 首页商品分类显示
router.register(r'indexgoods', IndexCategoryViewset, base_name="indexgoods")


# good_list = GoodsListViewset.as_view({
#     'get': 'list',
# })

from django.views.generic import TemplateView

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 第三方登录
    url('', include('social_django.urls', namespace='social')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^index/', TemplateView.as_view(template_name="index.html")),

    # drf自带认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt的auth
    url(r'^login/', obtain_jwt_token),

    # 商品列表页
    # url(r'goods/$', GoodsListView.as_view(), name="good-list"),
    # url(r'goodsset/$', good_list, name="good-list"),
    url(r'^', include(router.urls)),

    # 文档
    url(r'docs/', include_docs_urls(title="文档")),

    # 支付宝
    url(r'alipay/return/', AliPayView.as_view(), name="alipay"),
]
