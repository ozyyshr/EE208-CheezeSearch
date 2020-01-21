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

def get_books():
    f = open("tmp_index_books.txt", 'r')
    for line in f.readlines():
        a = line.strip()
        q.put(a)

def working():
    while True:
        books=q.get()
        print books
        count=0
        req = urllib2.Request(books)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1')
        content = urllib2.urlopen(req, timeout=60).read()
        soup = BeautifulSoup(content.decode('gb2312', errors='ignore'), "html.parser")
        books_page = books[31:48]
        for i in soup.find_all('a', {'name': "itemlist-picture"}):
            if(count>=60):
                break
            try:
                detail_page = i.get('href')
                book_pic = i.img.get('data-original')
                if (book_pic == None):
                    book_pic = i.img.get('src')
                name_tag = i.nextSibling
                book_title = name_tag.a.get('title').strip()

                detail_tag = name_tag.nextSibling
                detail = detail_tag.string
                if(detail==None):
                    continue
                detail=detail.strip()

                price_tag = detail_tag.nextSibling
                price = price_tag.find('span', {'class': 'search_now_price'})
                now_price = price.string[1:]
                pre_price = price.nextSibling.nextSibling.string[1:]

                author_tag = price_tag.nextSibling.nextSibling.nextSibling.nextSibling
                span = author_tag.find('span')
                authors_list=[]
                for y in span.find_all('a'):
                    authors_list.append(y.string)
                #date = span.nextSibling.string[2:]
                if (len(authors_list) == 0):
                    continue
                press = span.nextSibling.nextSibling.a.string
                print detail_page, book_pic

                comments_list = []
                item = detail_page[28:-5]
                comment_dict = 'http://product.dangdang.com/index.php?r=comment%2Flabel&productId=' + item + '&categoryPath=' + books_page + '&mainProductId=' + item
                req_1 = urllib2.Request(comment_dict)
                content_1 = urllib2.urlopen(req_1, timeout=60).read()
                soup_1 = BeautifulSoup(content_1, 'html.parser')
                json_r = json.loads(str(soup_1))
                for k in json_r['data']['tags']:
                    comments_list.append(k['name'])
                if(len(comments_list)==0):
                    continue

                classify_list = []
                req_2 = urllib2.Request(detail_page)
                content_2 = urllib2.urlopen(req_2, timeout=60).read()
                soup_2 = BeautifulSoup(content_2, 'html.parser')
                for j in soup_2.find_all('a', {'name': "__Breadcrumb_pub"})[1:]:
                    classify_list.append(j.string)
                if (len(classify_list) == 0):
                    continue

                book_page = 'http://product.dangdang.com/index.php?r=comment%2Flist&productId=' + item + '&categoryPath=' + books_page + '&mainProductId=' + item + '&tagId=1&long_or_short=short'
                req_3 = urllib2.Request(book_page)
                content_3 = urllib2.urlopen(req_3, timeout=60).read()
                soup_3 = BeautifulSoup(content_3, 'html.parser')
                pp = re.compile('goodRate":"\d*.\d*')
                rate = re.findall(pp, str(soup_3))[0][11:]

                if varLock.acquire():
                    #index_filename = 'index_books.txt'
                    folder = 'messages_books'
                    if not os.path.exists(folder):
                        os.mkdir(folder)
                    f = codecs.open(os.path.join(folder, 'book'+item+'.txt'), 'w')
                    f.write(codecs.BOM_UTF8)
                    f.write(book_title+'\n'+detail_page+'\n'+ book_pic+'\n'+now_price+'\n'+ pre_price+'\n'+ press+'\n'+rate+'\n'+detail+'\n')
                    for z in authors_list:
                        f.write(z+'\t')
                    f.write('\n')
                    for z in comments_list:
                        f.write(z + '\t')
                    f.write('\n')
                    for z in classify_list:
                        f.write(z + '\t')
                    f.write('\n')
                    f.close()
                    #index = open(index_filename, 'a')
                    #index.write('book'+item + '.txt'+'\n')
                    #index.close()
                    varLock.release()

                count+=1
            except Exception as e:
                print e
                continue
        q.task_done()

NUM = 10
varLock = threading.Lock()
q = Queue.Queue()
get_books()
for i in range(NUM):
    t = threading.Thread(target=working)
    t.setDaemon(True)
    t.start()
q.join()
time.sleep(3)



