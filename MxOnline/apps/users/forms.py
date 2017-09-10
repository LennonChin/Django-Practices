# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/09/10 下午 05:52'

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)