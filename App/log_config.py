# -*- coding: utf-8 -*- 
# Time : 2021/7/30 16:41 
# Author : Horace 
# File : log_config.py
# blog : horacehht.github.io

import logging

# 日志文件配置
# 日志记录器
user_log = logging.getLogger("user_log")
user_log.setLevel(logging.INFO)
sql_log = logging.getLogger("sql_log")
sql_log.setLevel(logging.DEBUG)
# 日志文件处理器
fh1 = logging.FileHandler(filename="log/user.log", mode='a')
fh2 = logging.FileHandler(filename="log/sql.log", mode="a")
# 日志格式器
fmt1 = logging.Formatter(fmt="%(asctime)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s")
fmt2 = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s"
                        , datefmt="%Y/%m/%d %H:%M:%S")
# 给处理器分配格式
fh1.setFormatter(fmt1)
fh2.setFormatter(fmt2)
# 记录器设置处理器
user_log.addHandler(fh1)
sql_log.addHandler(fh2)