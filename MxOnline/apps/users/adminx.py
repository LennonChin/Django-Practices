# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/09/09 下午 06:59'

import xadmin
from xadmin import views

from xadmin.plugins.auth import UserAdmin
from django.contrib.auth.models import User

from .models import EmailVerifyRecord, Banner, UserProfile


class UserProfileAdmin(UserAdmin):
    pass

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "后台管理系统"
    site_footer = "在线网"
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)

# xadmin.site.unregister(User)
# xadmin.site.register(UserProfile, UserProfileAdmin)
