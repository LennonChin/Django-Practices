# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/09/12 下午 09:52'

from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    my_field = forms.CharField()

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

