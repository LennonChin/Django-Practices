# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/09/12 下午 10:23'

from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView

urlpatterns = [

    # course list
    url(r'^list/$', CourseListView.as_view(), name="list"),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="detail"),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="info"),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="comment"),
    url(r'^add_comment/$', AddCommentView.as_view(), name="add_comment"),
]