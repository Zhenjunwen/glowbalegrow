#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 导入:
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import time


# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer, unique=True)
    name = Column(String(20))
    fullname = Column(String(40))
    create_time = Column(String(40))

class Iplog(Base):
    # 表的名字:
    __tablename__ = 'iplog'

    # 表的结构:
    id = Column(String(40), primary_key=True)
    ip = Column(String(20))
    domain = Column(String(20))
    request_time = Column(String(40))


class Apitest_domain(Base):
    # 表的名字:
    __tablename__ = 'apitest_domain'

    # 表的结构:
    id = Column(String(40), primary_key=True)
    Request_Method = Column(String(200))
    Request_URL = Column(String(200))
    Request_Headers = Column(String(200))
    Request_Params = Column(String(200))
    Request_Data = Column(String(200))