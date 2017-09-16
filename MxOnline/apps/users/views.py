# _*_ encoding: utf-8 _*_

from django.shortcuts import render

from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .forms import LoginForm, RegisterForm, ForgetForm, ModifyForm
from utils.email_send import send_register_email

from .models import UserProfile, EmailVerifyRecord

from utils.mixin_utils import LoginRequireMixin
# Create your views here.


# custom the auth method
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, 'login.html', {"msg": u"请先激活您的账户"})
            else:
                return render(request, 'login.html', {"msg": u"用户名或密码错误"})
        else:
            return render(request, 'login.html', {"login_form": login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get("email", "")
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {"register_form": register_form, "msg": u"用户已存在"})
            password = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.password = make_password(password)
            user_profile.is_active = False
            user_profile.save()

            # send mail
            send_register_email(username, "register")
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {"register_form": register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ForgetPasswordView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, "forget")
            return render(request, 'send_success.html')


class ResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPasswordView(View):
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            email = request.POST.get("email", "")
            password = request.POST.get("password", "")
            password2 = request.POST.get("password2", "")
            if password != password2:
                return render(request, 'password_reset.html', {'email': email, 'msg': u"密码不一致"})

            user = UserProfile.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'password_reset.html', {"modify_form": modify_form})


class UserInfoView(LoginRequireMixin, View):
    def get(self, request):
        context = {

        }
        return render(request, 'usercenter-info.html', context)


