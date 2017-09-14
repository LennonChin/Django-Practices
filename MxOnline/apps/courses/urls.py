# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/09/12 下午 10:23'

from django.conf.urls import url

from .views import CourseListView, CourseDetailView, InfoView

urlpatterns = [

    # course list
    url(r'^list/$', CourseListView.as_view(), name="list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="detail"),
    url(r'^info/(?P<course_id>\d+)/$', InfoView.as_view(), name="info"),
]