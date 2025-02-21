from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()  # 以pymsql为MySQLdb的代理

db = SQLAlchemy()
class Config:
    DEBUG = True  # 调试模式
    SQLALCHEMY_DATABASE_URI = 'mysql://<用户名>:<密码>@<主机>:<端口>/<数据库名>'  # 数据库连接
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 是否追踪数据库的修改