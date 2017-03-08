# #######################################################################
    # -*- encoding: utf-8 -*-
    # File Name: Login.py
    # Author: CirQ
    # mail: CirQ999@163.com
    # Created Time: 2017年03月07日 星期二 19时54分01秒
    # Description: 
# #######################################################################

import re
import json
import time
import base64
import urllib
import requests

class Login(object):
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0'
        })
        return

    def get_su(self):
        return base64.b64encode(urllib.quote(self.__username))

    def prelogin(self):
        preloginURL = "http://login.sina.com.cn/sso/prelogin.php"
        params = {
            "checkpin": "1",
            "entry": "mweibo",
            "su": "",
        }
        params["callback"] = "jsonpcallback%d"%int(time.time()*1000)
        self._session.get(preloginURL, params=params)
        params["callback"] = "jsonpcallback%d"%int(time.time()*1000)
        self._session.get(preloginURL, params=params)
        params["su"] = self.get_su()
        params["callback"] = "jsonpcallback%d"%int(time.time()*1000)
        resp = self._session.get(preloginURL, params=params)
        return json.loads(re.search(r"\((\{.*?\})\)", resp.text).group(1))

    def login(self):
        loginURL = "http://passport.weibo.cn/sso/login"
        data = {
            "username": self.__username,
            "password": self.__password,
            "savestate": "1",
            "r": "http://m.weibo.cn/",
            "ec": "0",
            "entry": "mweibo",
            "mainpageflag": "1",
        }
        self._session.headers.update({
            "Referer": "http://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F&sudaref=passport.weibo.cn&retcode=6102",
        })
        json = self._session.post(loginURL, data=data).json()
        if(json["retcode"] == 20000000):
            for tmpURL in json["data"]["crossdomainlist"].values():
                self._session.get("http:" + tmpURL)
            myURL = "http://weibo.cn/"
            self._session.get(myURL)
        return json

if __name__ == "__main__":
    weibo = Login("", "")

