# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/09/15 下午 11:11'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequireMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequireMixin, self).dispatch(request, *args, **kwargs)