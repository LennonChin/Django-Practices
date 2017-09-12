# _*_ encoding: utf-8 _*_
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
from MxOnline.settings import MEDIA_ROOT
import xadmin

from users.views import LoginView, RegisterView, ActiveUserView, ForgetPasswordView, ResetView, ModifyPasswordView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^login/$', LoginView.as_view(), name="user_login"),
    url(r'^register/$', RegisterView.as_view(), name="user_register"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPasswordView.as_view(), name="user_forget_password"),
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name="user_reset_password"),
    url(r'^modify_password/$', ModifyPasswordView.as_view(), name="user_modify_password"),

    # organization url settings
    url(r'^org/', include('organization.urls', namespace='org')),

    # opera media files
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]
