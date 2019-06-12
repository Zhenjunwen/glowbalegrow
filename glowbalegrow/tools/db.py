# coding: utf-8

# 导入:
from sqlalchemy import func, Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/oujn') #, echo=False
#engine = create_engine('mysql+mysqlconnector://root:123456@oujn.cc:3306/oujn') #, echo=False
# 创建DBSession类型:
session_factory = sessionmaker(bind=engine)
# scoped_session保证每个线程获得的 session 对象都是唯一的
DBSession = scoped_session(session_factory)


