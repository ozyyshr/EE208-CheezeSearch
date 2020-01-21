# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import os
import sys
import urlparse
import threading
import Queue
import time
import json
import codecs
reload(sys)
sys.setdefaultencoding('utf8')

def first_crawl(seed):
    pages = []
    req = urllib2.Request(seed)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
    content = urllib2.urlopen(req, timeout=60).read()
    soup = BeautifulSoup(content, 'html.parser')
    p = re.compile('http://category.dangdang.com/cp01.*(.html)$')
    for i in soup.find_all('a', {'href': p}):
        urll = str(i.get('href'))[34:48] #截取url的编号部分
        if (urll not in pages):
            pages.append(urll)
    p1 = re.compile('http://book.dangdang.com/01.*')
    p2 = re.compile('01...')
    for i in soup.find_all('a', {'href': p1}):
        ur = str(re.findall(p2, i.get('href'))[0])[3:] + '.00.00.00.00'
        if ur not in pages:
            pages.append(ur)
    return pages


def second_crawl(pages):
    index_filename = 'tmp_index_books.txt'
    for page in pages:
        url = 'http://category.dangdang.com/cp01.' + page + '.html'
        index = open(index_filename, 'a')
        index.write(url+ '\n')
        index.close()


if __name__ == '__main__':
    pages = first_crawl('http://book.dangdang.com/?_utm_brand_id=11106&_ddclickunion=460-5-biaoti|ad_type=0|sys_id=1')
    second_crawl(pages)