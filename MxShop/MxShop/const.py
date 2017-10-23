# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/10/18 20:27'

import os
import sys
from MxShop.settings import *


# 手机号码正则
REGEX_MOBILE = "0?(13|14|15|18)[0-9]{9}"

# 云片网设置
yunpian_apikey = "d6c4ddbf50ab36611d2f52041a0b949e"

# 支付宝支付相关
private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/private_2048.txt')
alipay_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/alipay_pub_key.txt')