#!/usr/bin/env python
# encoding: utf-8
"""
@author:     idhyt
@copyright:  2015 kingsoft. All rights reserved.
@contact:    idhytgg@gmail.com
@date:       2015年4月2日
@description:
"""
import urllib2
import re


class UrlParse(object):
    def __init__(self):
        # 判断是否是http://www.ssss.com/?id=3的形式。同时增加判断，url大于512字节认为不可靠，过滤掉
        pass
    
    def get_params(self, url, payload="=ADC22F"):
        query = urllib2.urlparse.urlparse(url).query
        params = query.split("&")
        test_params = {}
        
        for i in params:
            if i == params[0]:
                if "=" not in i:
                    test_params["?"+i] = "?" + i + payload
                elif i.endswith("="):
                    test_params["?"+i] = "?" + i + payload
                else:
                    # test_params["?"+i] = "?" + i.replace(i[i.rindex("=")+1:], payload)
                    test_params["?"+i] = "?" + i + payload
            else:
                if "=" not in i:
                    test_params["&"+i] = "&" + i + payload
                elif i.endswith("="):
                    test_params["&"+i] = "&" + i + payload
                else:
                    # test_params["&"+i] = "&"+ i.replace(i[i.rindex("=")+1:], payload)
                    test_params["&"+i] = "&" + i + payload
        return test_params
    
    def is_param_url(self, url, regex=r"http://[\w./]*\?[\w-]*="):
        # pattern = re.compile(r'http://[0-9a-zA-Z._/]*\?[a-zA-Z_]*=[0-9a-zA-Z_]*[0-9a-zA-Z._/=&]*')
        pattern = re.compile(regex, re.IGNORECASE)
        match = pattern.match(url)
        if match:
            return True
        else:
            return False
        
    # 判断是否有无法解析的url，比如一些doc文档。
    def is_valid_url(self, url):
        if len(url) >= 512:
            return False
        pat = re.compile(r'[0-9a-zA-Z._/\?:=&@]*\.(jpg|swf|gif|cer|png|doc|xls|ppt|pptx|docs|rar|zip|pdf|chm|apk)')
        match = pat.match(url)
        if match:
            return False
        else:
            return True




