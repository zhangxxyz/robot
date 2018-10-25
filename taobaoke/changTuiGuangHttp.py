#没有api权限 自主用爬虫获取推广链接
import requests
import json


UA = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
proxies = {"http":"110.73.11.207:8123"}
cook ="t=955b4a322a0360af56011daf9a963bcd; cna=l4G3EtN4lnMCAW/GR41O7k13; account-path-guide-s1=true; 32900145_yxjh-filter-1=true; cookie2=1299a13258e3a79487508756f4dce85f; v=0; _tb_token_=33f77e660efe; alimamapwag=TW96aWxsYS81LjAgKE1hY2ludG9zaDsgSW50ZWwgTWFjIE9TIFggMTBfMTNfNCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzY5LjAuMzQ5Ny4xMDAgU2FmYXJpLzUzNy4zNg%3D%3D; cookie32=6e353e44dcb2ada023d98f7c1d920912; alimamapw=SF1RX1cKVQpWVwoEVlxsAlcGBgNRBgcCAAxUXQFXB1UGAVVRAVcBBgFUVggHAVE%3D; cookie31=MzI5MDAxNDUsemhhbmc4NzM1MzkwNzksODk2OTk4MDFAcXEuY29tLFRC; login=VFC%2FuZ9ayeYq2g%3D%3D; rurl=aHR0cHM6Ly9wdWIuYWxpbWFtYS5jb20v; apush33cf35cc5200d8c89f65e8649c606a77=%7B%22ts%22%3A1537843977927%2C%22heir%22%3A1537843908281%2C%22parentId%22%3A1537843904757%7D; isg=BCAgkW8ob8r199PFWrKMawGa8SgygQSVewmPSpoz6jvOlca_QDgGghFjKX2wJbzL"
# http://item.taobao.com/item.htm?id=557635861446
requestUrl = "https://pub.alimama.com/urltrans/urltrans.json?siteid=121950227&adzoneid=28160100255&promotionURL=https%3A%2F%2Fitem.taobao.com%2Fitem.htm%3Fspm%3Da219t.7900221%2F10.1998910419.d5d3d3cdd.19a975a5bN5XVB%26id%3D564775176010%26spm%3Da219t.7900221%2F10.1998910419.d5d3d3cdd.19a975a5bN5XVB&t=1537843978444&pvid=52_111.198.24.246_451_1537843919377&_tb_token_=33f77e660efe&_input_charset=utf-8"

Cookies ={}

def getCookiesDict():
    if len(Cookies)>0:
        return Cookies
    for dict in cook.split(";"):
        key,value = dict.split('=',1)
        Cookies[key] = value
    return Cookies

def getHttp():
    res = requests.get(requestUrl,proxies=proxies,cookies=getCookiesDict(),headers=UA)
    dict=res.json()
    print(dict)
# getHttp()
# queryGoods.content()

