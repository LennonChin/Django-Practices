# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/09/12 下午 10:23'

from django.conf.urls import url, include
from .views import OrgView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavoriteView
from .views import TeacherListView, TeacherDetailView

urlpatterns = [

    # 课程机构首页
    url(r'^list/$', OrgView.as_view(), name="list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="course"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="desc"),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="teacher"),

    # favorite org
    url(r'^add_fav/$', AddFavoriteView.as_view(), name="add_fav"),

    # teacher相关
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]