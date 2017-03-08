# #######################################################################
    # -*- encoding: utf-8 -*-
    # File Name: Keek.py
    # Author: CirQ
    # mail: CirQ999@163.com
    # Created Time: 2017年03月07日 星期二 22时47分42秒
    # Description: 
# #######################################################################

import time
from Login import Login
from bs4 import BeautifulSoup

class Keek(Login):
    def __init__(self, username, password, path):
        super(self.__class__, self).__init__(username, password)
        self.__to = path
        return


    def topage(self, page=1):
        url = "http://weibo.cn/%s?page=%d" % (self.__to, page)
        self.__page = self._session.get(url).text
        return
    

    def parsepage(self, From=1, To=1):
        for i in range(From, To+1):
            self.topage(i)
            soup = BeautifulSoup(self.__page, "html.parser")
            items = soup.find_all("div", attrs={"class":"c","id":True})
            for item in items:
                msg = self.parseitem(item)
                if msg is not None:
                    print msg, "\n\n"
                else:
                    print "None\n\n"
                time.sleep(1)
        return


    def parseitem(self, item):
        ct, ctt = "", ""
        for i in item.select(".ctt")[0].stripped_strings:
            ctt = "%s%s " % (ctt, i)
        for i in item.select(".ct")[0].stripped_strings:
            ct = "%s%s" % (ct, i)
            
        if len(item)==1 or len(item)==2:
            if item.select(".cmt"):  #转发不带图片
                try:
                    ss = item.select(".cmt")[0].stripped_strings
                    ss.next()
                    ori = ss.next()
                except StopIteration:
                    ori = u"已删除"
                ss = item.contents[1].stripped_strings
                ss.next()
                rea = ss.next()
                return u"%s:\n转发 %s 的微博：%s\n转发理由：%s" % (ct, ori, ctt, rea)
            else:  #原创
                if item.find("img"):
                    img = item.find("img")["src"]
                    return u"%s:\n发布微博：%s\n图片：%s" % (ct, ctt, img)
                else:
                    return u"%s:\n发布微博：%s" % (ct, ctt)
        elif len(item)==3:  #转发带图片
            ss = item.select(".cmt")[0].stripped_strings
            ss.next()
            ori = ss.next()
            ss = item.contents[2].stripped_strings
            ss.next()
            rea = ss.next()
            img = item.find("img")["src"]
            return u"%s:\n转发 %s 的微博：%s\n原文图片：%s\n转发理由：%s" % (ct, ori, ctt, img, rea)
        else:
            return None





if __name__ == "__main__":
    hi = Keek("username", "password", "tothisid")
    hi.login()
    hi.parsepage(To=5)
