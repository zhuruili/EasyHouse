from flask_sqlalchemy import SQLAlchemy
import pymysql
from dotenv import load_dotenv
import os

pymysql.install_as_MySQLdb()  # 以pymsql为MySQLdb的代理

load_dotenv()  # 从.env文件中加载环境变量

db = SQLAlchemy()  # 实例化SQLAlchemy

class Config:
    DEBUG = True  # 调试模式
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_DATABASE = os.getenv('DB_DATABASE')
    SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@localhost:3306/{DB_DATABASE}'  # 数据库连接
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 是否追踪数据库的修改