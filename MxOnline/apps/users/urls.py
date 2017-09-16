# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/09/16 下午 10:03'

from django.conf.urls import url

from .views import UserInfoView, UploadImageView, UpdatePasswordView

urlpatterns = [

    url(r'^info/', UserInfoView.as_view(), name='info'),
    url(r'^image/upload/', UploadImageView.as_view(), name='image_upload'),
    url(r'^update/password/', UpdatePasswordView.as_view(), name='update_password'),
]