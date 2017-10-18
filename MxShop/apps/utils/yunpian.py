# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/10/18 20:02'

import requests


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "您的验证码是{code}".format(code=code)
        }
        response = requests.post(self.single_send_url, data=params)
        import json
        result_dict = json.loads(response.text)
        return result_dict


if __name__ == "__main__":
    yun_pian = YunPian("d6c4ddbf50ab36611d2f52041a0b949e")
    yun_pian.send_sms("2017", "13381947550")