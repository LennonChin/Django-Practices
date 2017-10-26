# _*_ coding: utf-8 _*_
__author__ = 'LennonChin'
__date__ = '2017/10/26 20:58'


def get_auth_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_uri = "http://www.coderap.com:8000/complete/weibo/"
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_uri={redirect_uri}".format(client_id="3793839728",
                                                                                            redirect_uri=redirect_uri)
    print(auth_url)


def get_access_token(code="42a7b1974d16117d0ecd3a9f481be5d6"):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    import requests
    request_dict = {
        "client_id": "3793839728",
        "client_secret": "62c7ec67fea66535d0584f3722caa44b",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://www.coderap.com:8000/complete/weibo/"
    }
    result_dict = requests.post(access_token_url, data=request_dict)
    print(result_dict)
    # b'{"access_token":"2.00dXSZ_E3BZkIEcde86a70e0gqPMvC","remind_in":"157679999","expires_in":157679999,"uid":"3953694469","isRealName":"true"}'


def get_user_info(access_token, uid):
    user_url = "https://api.weibo.com/2/users/show.json?access_token={token}&uid={uid}".format(token=access_token, uid=uid)
    print(user_url)

if __name__ == "__main__":
    # get_auth_url()
    # get_access_token(code="42a7b1974d16117d0ecd3a9f481be5d6")
    get_user_info(access_token="2.00dXSZ_E3BZkIEcde86a70e0gqPMvC", uid="3953694469")