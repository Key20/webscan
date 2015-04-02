Web Scan  
Author: idhyt  
Mail: idhytgg@gmail.com

web 扫描器 xss & sql & 网站目录

编写环境： Python_2.75_32 & PyChram


目录结构：
```
webscan
│  
│  webscan.py                                             ----启动模块
│  webscan.bat                                            ----启动脚本
│  
├─config
│      
│      config.py                                          ----配置文件
│      
├─lib
│  │  
│  ├─core                                                 ----核心代码
│  │  │  
│  │  ├─sitedir                                           ----网站目录扫描
│  │  │  │  site_dir_scan.py
│  │  │  │ 
│  │  │  ├─dict
│  │  │  │      cgi.txt
│  │  │  │      cgi1.txt
│  │  │  │      
│  │  │  └─exts
│  │  │          status_code.json
│  │  │          
│  │  ├─sqlinject                                         ----sql注入模块
│  │  │      sql_payloads.json
│  │  │      sql_scan.py
│  │  │      
│  │  ├─webkit
│  │  │      webkit.py                                    ----webkit模块(暂未使用)
│  │  │      
│  │  └─xss                                               ----xss扫描模块
│  │          xss_payloads.json
│  │          xss_scan.py
│  │          
│  ├─parse                                                ----解析模块包
│  │      data.py
│  │      url.py
│  │      web.py
│  │      
│  └─scan                                                 ----扫描方式及任务分发
│          urlscan.py
│          urlsscan.py
├─proxy                                                   ----socket5代理
│      plink.exe
│      plink_init.bat
│      proxy_switch.py
│      socks.py
│      
├─public
│  │  
│  ├─log                                                  ----日志模块
│  │  │  log.py
│  │  │  
│  │  └─logger
│  │          Logger.py
│  │          
│  └─publish                                              ----结果发布模块
│          result2html.py
│          
├─sql                                                     ----数据库操作模块
│      databases.py
│      mysql.py
│      
└─thirdparty                                              ----第三方库
    │  
    └─requests
        │  
'''

更新说明：

-2015.04.02 代码结构重新整理。
-2015.03.26 增加网站目录扫描。
-2015.03.24 增加socket5切代理模块,加入sql注入扫描。
-2015.03.19 增加扫描来源。
-2015.03.13 xss扫描,升级为requests 模块，并添加cookies。 

其他：
-pyayloads中，BetweenScript 和 InScript 中的```x55test```误报较高，如不需要可自行去掉。（建议保留，这两个payload 有时会带来惊喜～）

用法:
 
对于单个url：
webscan.py -u "http://127.0.0.1/xss.php?x" -c cookies.txt
其中 cookies.txt 为你访问目标站点时的cookies

多url,默认从数据库读取
webscan.py -m 3 -s 1
'''
-m 扫描模式 01 xss; 10 sql; 11 both
-s urls来源 01 数据库; 其他保留,可自动添加
'''

result:
[utf-7] [+/v8 +ADw-x55test+AD4-]: http://127.0.0.1/xss.php?x=%2B/v8%20%2BADw-x55test%2BAD4-
[betweenCommonTag] [--><x55test>]: http://127.0.0.1/xss.php?x=--%3E%3Cx55test%3E
[betweenCommonTag] [<x55test>]: http://127.0.0.1/xss.php?x=%3Cx55test%3E
[inCommonAttr] [" x55test=x55]: http://127.0.0.1/xss.php?x=%22%20x55test%3Dx55
[betweenScript] [x55test(1)]: http://127.0.0.1/xss.php?x=x55test%281%29
[inCommonAttr] ["><x55test>]: http://127.0.0.1/xss.php?x=%22%3E%3Cx55test%3E
[inCommonAttr] ['><x55test>]: http://127.0.0.1/xss.php?x=%27%3E%3Cx55test%3E
[inCommonAttr] [><x55test>]: http://127.0.0.1/xss.php?x=%3E%3Cx55test%3E


扫描完毕后，会在目录下生结果文件，文件名为当前日期，如2015-01-11-21-23-27

'''