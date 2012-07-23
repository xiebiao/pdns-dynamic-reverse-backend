#!/usr/bin/env python 
# --*-- coding: utf-8 --*--

#import _mysql
import MySQLdb
import time
import argparse

parser = argparse.ArgumentParser(description='Use "-i" for insert data,"-t" for truncate data.')
parser.add_argument("-t",action="store_true",help="truncate data")
parser.add_argument("-i",action="store_true",help="insert data")
_insert = parser.parse_args().i
_truncate = parser.parse_args().t

if (not  _insert) and (not _truncate):
    parser.print_help()
    import sys
    sys.exit(0)

_MYSQL_HOST="10.28.168.163"
_MYSQL_USER="pdns"
_MYSQL_PASSWORD="pdns"
_MYSQL_DB="pdns"
_TTL="68400"
_A="10.28.164.231"

dns_file = open("test",'r')

def insert():
    lines = dns_file.readlines()
    con = get_connection()
    cursor = con.cursor()
    for line in lines:
        linea = line.split(" ")
        domain = linea[0]
        param = (domain,"MASTER")
        sql = "insert into domains (name,type) values(%s,%s)"
        cursor.execute(sql,param)
        sql_id = "select id from domains order by id desc limit 1 "
        cursor.execute(sql_id)
        rs = cursor.fetchone()
        domain_id=rs[0]
        sql_record="""insert into records
        (domain_id,name,type,content,ttl,prio,change_date) values
        (%s,%s,%s,%s,%s,%s,%s)"""
        param = (domain_id,
                domain,
                "SOA",
                " 2012071800 28800 7200 604800 86400",
                _TTL,
                "0",
                time.time())
        param_a = (domain_id,
                domain,
                "A",
                _A,
                _TTL,
                "0",
                time.time())
        print param
        print param_a
        cursor.execute(sql_record,param)
        cursor.execute(sql_record,param_a)
        con.commit()
    close(con)

def truncate():
    sql1 = "truncate table domains"
    sql2 = "truncate table records"
    con1 = get_connection()
    con1.query(sql1)
    con2 = get_connection()
    con2.query(sql2)
    print "%s\n%s" % (sql1,sql2)
    close(con1)
    close(con2)

def close(connection):
    connection.close()

def get_connection():
    connection =MySQLdb.connect(
        _MYSQL_HOST,
        _MYSQL_USER,
        _MYSQL_PASSWORD,
        _MYSQL_DB)
    return connection

if __name__   == "__main__":
    if _insert == True :
        insert()
    if _truncate == True:
        truncate()
