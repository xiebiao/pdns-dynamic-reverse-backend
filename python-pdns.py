#!/usr/bin/env python
# --*-- coding: utf-8 --*--

"""
Powerdns 配置 :

launch=pipe
pipebackend-abi-version=1 # t1  protocol
pipe-command=the path of this script 
pipe-regex=   #可以配置pipe匹配模式

""" 

import sys, os
import re
import syslog
import time

TTL=3600
VERSION="t1"

def parse(stdin, stdout):
    line = stdin.readline().strip()
    if not line.startswith('HELO'):
        print >>stdout, 'FAIL'
        stdout.flush()
        syslog.syslog('Received "%s", expected "HELO"' % (line,))
        sys.exit(1)
    else:
        print >>stdout, '%s is working!' % (os.path.basename(sys.argv[0]),)
        stdout.flush()

    while True:
        line = stdin.readline().strip()
        if not line:
            break

        #print >>stdout, 'LOG\tline: %s' % line
        question = line.split('\t')
        if len(question) < 6:
            print >>stdout,'Error protocol'
            continue
        # t1 protocol
        # Q  qname       qclass  qtype   id  remote-ip-address
        qkind,qname,qclass,qtype,qid,qrip = question
        # t2 protocol
        # Q qname       qclass   qtype   id  remote-ip-address   local-ip-address 
        # qkind,qname,qclass,qtype,qid,qrip,qlip = question
        # t3 protocol
        # Q qname       qclass   qtype id remote-ip-address local-ip-address edns-subnet-address
        # qkind,qname,qclass,qtype,qid,qrip,qlip,qedns= question

        # 处理特定的记录
        if qtype in ["SOA","ANY"] and qname.startswith('www.example'):
            ttl=3600
            content="2008080300 1800 3600 604800 3600"
            response ='DATA\t%s\t%s\tSOA\t%d\t-1\t%s' % (qname, qclass, ttl,content,)
            print >>stdout,response

        if qtype in ["A","ANY"]: 
            IP="10.28.1.1"
            print >>stdout, 'DATA\t%s\t%s\tA\t%d\t-1\t%s' % \
                         (qname, qclass, TTL,IP,)

        print >>stdout,"END"
        stdout.flush()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(parse(sys.stdin, sys.stdout))
