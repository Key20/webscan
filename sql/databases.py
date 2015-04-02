#!/usr/bin/env python
# encoding: utf-8
"""
@author:     idhyt
@copyright:  2015 kingsoft. All rights reserved.
@contact:    idhytgg@gmail.com
@date:       2015年3月18日
@description:
"""
import mysql
from public.log import log


class ScanInfo(object):
    def __init__(self, sql_info):
        self.cloud_db = (sql_info.db_host, sql_info.db_user, sql_info.db_pwd, sql_info.db_name)
        self.db_table = sql_info.db_table
        
    # function : get value from db (数据库信息, 保留)
    # return : (value1, value2, value3...)  
    def select_info(self, tag=0):
        try:
            sql = mysql.MySQL(*self.cloud_db)
            if tag == 0:
                sql_string = "SELECT id, file_name, uri" + \
                             " FROM " + self.db_table + \
                             " WHERE xss_state LIKE 0 AND sql_state LIKE 0 LIMIT 1"
            if tag == 1:
                sql_string = ""
            ret_tuple = sql.get_value(sql_string)
            if ret_tuple is not None: 
                sql_string = "UPDATE " + self.db_table + \
                             " SET xss_state = 1, sql_state = 1" + \
                             " WHERE id LIKE " + str(ret_tuple[0])
                sql.insert_value(sql_string)
                return ret_tuple
            
            return None
        except Exception, e:
            log.output_log("[error] " + str(e))
            return None
        
    # tag = 0 xss
    # tag = 1 sql
    def insert_info_s(self, insert_info_list, tag = 0):
        try:
            sql = mysql.MySQL( *self.cloud_db )
            if tag == 0:
                for insert_info in insert_info_list:
                    vul_detail = insert_info[3].replace("'", "\\'")
                    sql_string = "INSERT INTO " + self.db_table + "(scan_id, file_name, vul_type, vul_detail, vul_url) values(" + \
                                 str(insert_info[0]) + ", '" + \
                                 insert_info[1] + "', '" + \
                                 insert_info[2] + "', '" + \
                                 vul_detail + "', '" + \
                                 insert_info[4] + "')"
                    sql.insert_value_not_commit(sql_string)
                sql.commit()
                
            elif tag == 1:
                sql_string = ''
                sql.insert_value(sql_string)
            return True
        
        except Exception, e:
            log.output_log("[error] " + str(e))
            return False

    def get_scan_uri(self):
        return self.select_info()
    
    # (index_by_scan_info_id, file_name, vul_type, vul_uri, vul_detail)
    def save_vul_info(self, insert_info_list):
        self.insert_info_s(insert_info_list)

