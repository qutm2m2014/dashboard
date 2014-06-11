# -*- coding: utf-8 -*-


class ProductionConfig():
    SQLALCHEMY_DATABASE_URI = "postgresql://m2m:@m2m2014@pg.qutm2m.com:5432/m2m"
    SQLALCHEMY_ECHO = False
    DEBUG = False


class DevConfig():
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "postgresql://m2m:@m2m2014@pg.qutm2m.com:5432/m2m"
