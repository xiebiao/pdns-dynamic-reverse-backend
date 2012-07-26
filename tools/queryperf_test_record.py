#!/usr/bin/env python 
# --*-- coding: utf-8 --*--
"""
    生成queryperf压力测试文件
"""
import os
import _mysql
import random

_DNS_TEST_FILE="test"
_DNS_RECORDS=10000
_DOMAIN_LENGTH=10

def get_random_string(n):

    st=''
    while len(st)<n:
        temp= chr(97+random.randint(0,25))
        if st.find(temp)==-1:
            st = st.join(['',temp])
    return st

def create_test_file():
    
    test_file = open(_DNS_TEST_FILE,'w+') 
    dns_records = _DNS_RECORDS
    while dns_records > 0:
        dns_records = dns_records - 1 
        n = random.randint(1,_DOMAIN_LENGTH)
        domain="www."+ get_random_string(n)+ str(dns_records) +".com A\n" 
        #print domain
        test_file.write(domain)

    test_file.close()

create_test_file()

