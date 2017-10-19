from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from .serializers import SmsSerializer, UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from utils.yunpian import YunPian
from MxShop.const import yunpian_apikey
from .models import VerifyCode

from random import choice

User = get_user_model()

# Create your views here.


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True) # status 400

        mobile = serializer.validated_data["mobile"]

        code = self.generate_code()

        yun_pian = YunPian(yunpian_apikey)
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:

            # 保存验证码
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()

            context = {
                "mobile": sms_status["msg"]
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        else:
            context = {
                "mobile": mobile
            }
            return Response(context, status.HTTP_201_CREATED)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        result_dict = serializer.data
        payload = jwt_payload_handler(user)
        result_dict["token"] = jwt_encode_handler(payload)
        result_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(result_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()