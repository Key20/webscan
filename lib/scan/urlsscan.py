#!/usr/bin/env python
# encoding: utf-8
"""
@author:     idhyt
@copyright:  2015 kingsoft. All rights reserved.
@contact:    idhytgg@gmail.com
@date:       2015年3月19日
@description:
"""
import time
from public.log import log
from sql import databases
from config import config

from lib.core.sqlinject import sql_scan
from lib.core.xss import xss_scan
from lib.core.sitedir import site_dir_scan
from lib.parse import url as urlparse
from lib.parse import data


class UrlsScan(object):
    def __init__(self, cookie_file, url_src, scan_mode=1, is_proxy=0):
        
        self.scan_mode = scan_mode
        self.cookie_file = cookie_file
        self.url_src = url_src
        self.is_proxy = is_proxy
        self.proxy = None
        
        self.data_parse = data.Data()
        self.url_parse = urlparse.UrlParse()
        
        self.urls_scan_go()
        
    def urls_scan_go(self):
        """
        log.output_log("[aaaa] cccccc")
        log.output_log("[write] cccccc", True)
        """
        # init
        cookies = self.data_parse.get_cookies(self.cookie_file) if self.cookie_file is not None else None
        
        # set proxy
        if self.is_proxy == 1:
            from proxy import proxy_switch
            self.proxy = proxy_switch.Proxy()
            proxy_switch.link_proxy(self.proxy)
            
        if self.url_src == 1:
            self.scan_db_urls(cookies)

    def scan_db_urls(self, cookies):
        # 存储类方法初始化
        vul_db_cfg = config.VulInfoDB()
        vul_db_op = databases.ScanInfo(vul_db_cfg)
        
        # 扫描类方法初始化
        scan_db_cfg = config.ScanInfoDB()
        scan_db_op = databases.ScanInfo(scan_db_cfg)
        
        # 开始扫描
        # 获取扫描链接
        while True:
            scan_info_tuple = scan_db_op.get_scan_uri()
            if scan_info_tuple is None:
                log.output_log("[*] no url in db, please wait......")
                time.sleep(1*60*60)
                continue
            
            url, insert_info = scan_info_tuple[2], scan_info_tuple[:-1]
            if self.url_parse.is_param_url(url) is False:
                continue
            log.output_log("[*] begin scan url " + url, True)
            
            # xss scan
            if self.scan_mode & 1:
                log.output_log("[*] test xss...")
                xss = xss_scan.XssScan(url, cookies, self.proxy)
                if len(xss.result) > 0:
                    # # 打印，存文件
                    # parse.output_result(xss.result)
                    xss_info_list = self.data_parse.format_vul_info(xss.result, insert_info)
                    # 漏洞存数据库
                    vul_db_op.save_vul_info(xss_info_list)
                else:
                    log.output_log("[xss] not found xss")
      
            # sql scan
            if self.scan_mode & 2:
                log.output_log("[*] test sql inject...")
                sql = sql_scan.SqlScan(url, self.proxy)
                if len(sql.result) > 0:
                    # # 打印，存文件
                    # parse.output_result(sql.result)
                    sql_info_list = self.data_parse.format_vul_info(sql.result, insert_info)
                    # 漏洞存数据库
                    vul_db_op.save_vul_info(sql_info_list)
                else:
                    log.output_log("[sql] not found inject")
    
            # site dir scan
            if self.scan_mode & 4:
                log.output_log("[*] test site dir...")
                site_dir = site_dir_scan.SiteDirScan(url, self.proxy)
                if len(site_dir.result) > 0:
                    pass
