#encoding:utf-8
import sys
sys.path.append('..')
import scraper
import sqlite3

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class DBManager(object):
    """This is a singleton class"""
    
        