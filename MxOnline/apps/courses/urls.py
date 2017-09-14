# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/09/12 下午 10:23'

from django.conf.urls import url

from .views import CourseListView, CourseDetailView

urlpatterns = [

    # course list
    url(r'^list/$', CourseListView.as_view(), name="list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="detail"),
]