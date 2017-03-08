# KEEK_WEIBO
This is a web crawler project that simulates the login procedure in Weibo and then fetch someone's post message on his/her Weibo.

---

爬取新浪微博可分网页版或移动版。

[网页版](http://weibo.com/)可以以游客身份访问其他用户的主页，但抓取的过程较麻烦。网页版的内容是由JS发送的，无法使用html解析库实现查找。

[移动版](http://weibo.cn)第一步是模拟登录，请求不频繁时，不需要提交验证码，因而可以方便地登陆并抓取信息。
网页版的模拟登录先一步实现了，但因为发现网页抓取较难，故转向移动版。网页版模拟登录代码没有在此处发布出来。
由于新浪是使用SSO系统实现全站登陆权限发放的，因而网页版登陆后也（应该）可以在移动版上抓取信息，没有实现该功能。

---

登录后抓取的信息单元可以分为四种情况，对应于`parseitem(item)`的四种不同的返回情况，不表。

所有代码没有考虑网络情况，对于可能发生的异常没有捕获（反正也只是自己做着玩的）。
