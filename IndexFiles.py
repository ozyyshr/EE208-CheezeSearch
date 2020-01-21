# -*- coding: UTF-8 -*-
# !/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time
import re
from datetime import datetime
from urlparse import *

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

import jieba

import time
import threading

import os
import sys
import urllib2

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""


class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)


class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, storeDir):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(writer)
        ticker = Ticker()
        print 'commit index'
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, writer):
        visited = []
        judge = "~!@#$%^&*()_+-*/<>,.[]\/"

        t1 = FieldType()
        t1.setIndexed(False)
        t1.setStored(True)
        t1.setTokenized(False)

        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        cnt = 0

        fileList = os.listdir('messages_books')
        for f in fileList:
            file = open('messages_books/' + f, 'r')
            title = file.readline()
            print title

            url = file.readline()
            if url in visited:
                continue
            visited.append(url)
            cnt += 1
            image = file.readline()
            price = file.readline()
            originalprice = file.readline()
            editor = file.readline()
            rating = file.readline()
            description = file.readline()
            authors = file.readline()
            comments = file.readline()
            categories = file.readline()

            print "adding", title
            try:
                print cnt
                doc = Document()
                doc.add(Field("title", title, t1))
                doc.add(Field("url", url, t1))
                doc.add(Field("image", image, t1))
                doc.add(Field("price", price, t1))
                doc.add(Field("originalprice", originalprice, t1))
                doc.add(Field("editor", editor, t2))
                doc.add(Field("rating", rating, t1))
                doc.add(Field("description", description, t1))
                doc.add(Field("authors", authors, t1))
                authors1 = authors.split('\t')
                authors1 = ' '.join(authors1)
                doc.add(Field("authors1", authors1, t2))
                doc.add(Field("comments", comments, t1))
                doc.add(Field("categories", categories, t1))

                image = re.findall(r'[^\*"/:?\\|<>]', image, re.S)
                image = "".join(image)
                doc.add(Field("image1", image, t2))

                categories = categories.split('\t')
                categories = ' '.join(categories)

                seg_title = jieba.cut(title, cut_all=False)
                title = ' '.join(seg_title)
                seg_editor = jieba.cut(editor, cut_all=False)
                editor = ' '.join(seg_editor)
                seg_categories = jieba.cut(categories, cut_all=False)
                categories = ' '.join(seg_categories)

                if title:
                    doc.add(Field("title1", title, t2))
                else:
                    print "warning: no title in %s" % url
                if editor:
                    doc.add(Field("editor1", editor, t2))
                else:
                    print "warning: no editor in %s" % url
                if categories:
                    doc.add(Field("categories1", categories, t2))
                else:
                    print "warning: no editor in %s" % url
                writer.addDocument(doc)
            except Exception, e:
                print "Failed in indexDocs:", e
            file.close()

        for i in range(0, 1739):

            with open('book' + '/' + 'book' + str(i) + '.txt', 'r') as file:
                title = file.readline()
                print title
                url = file.readline()
                if url in visited:
                    continue
                visited.append(url)
                cnt += 1
                image = file.readline()
                price = file.readline()
                originalprice = file.readline()
                editor = file.readline()
                for i in editor:
                    if i in judge:
                        editor = ''
                        break
                rating = file.readline()
                description = file.readline()
                authors = file.readline()

                comments = file.readline()
                categories = file.readline()


                print "adding", title
                try:
                    print cnt
                    doc = Document()
                    doc.add(Field("title", title, t1))
                    doc.add(Field("url", url, t1))
                    doc.add(Field("image", image, t1))
                    doc.add(Field("price", price, t1))
                    doc.add(Field("originalprice", originalprice, t1))
                    doc.add(Field("editor", editor, t1))
                    doc.add(Field("rating", rating, t1))
                    doc.add(Field("description", description, t1))
                    doc.add(Field("authors", authors, t1))
                    authors1 = authors.split('\t')
                    for author in authors1:
                        author = author.split('(')[0]
                        author = re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", " ", author)
                    authors1 = ' '.join(authors1)
                    doc.add(Field("authors1", authors1, t2))
                    doc.add(Field("comments", comments, t1))
                    doc.add(Field("categories", categories, t1))

                    image = re.findall(r'[^\*"/:?\\|<>]', image, re.S)
                    image = "".join(image)
                    doc.add(Field("image1", image, t2))

                    categories = categories.split('\t')
                    categories = ' '.join(categories)

                    seg_title = jieba.cut(title, cut_all=False)
                    title = ' '.join(seg_title)
                    seg_editor = jieba.cut(editor, cut_all=False)
                    editor = ' '.join(seg_editor)
                    seg_categories = jieba.cut(categories, cut_all=False)
                    categories = ' '.join(seg_categories)

                    if title:
                        doc.add(Field("title1", title, t2))
                    else:
                        print "warning: no title in %s" % url
                    if editor:
                        doc.add(Field("editor1", editor, t2))
                    else:
                        print "warning: no editor in %s" % url
                    if categories:
                        doc.add(Field("categories1", categories, t2))
                    else:
                        print "warning: no editor in %s" % url
                    writer.addDocument(doc)
                except Exception, e:
                    print "Failed in indexDocs:", e

        for i in range(0, 2333):

            with open('files' + '/' + 'book' + str(i) + '.txt', 'r') as file:
                title = file.readline()
                print title
                url = file.readline()
                if url in visited:
                    continue
                visited.append(url)
                cnt += 1
                image = file.readline()
                price = file.readline()

                editor = file.readline()
                for i in editor:
                    if i in judge:
                        editor = ''
                        break
                rating = file.readline()
                description = file.readline()
                authors = file.readline()
                comments = file.readline()
                categories = file.readline()

                print "adding", title
                try:
                    print cnt
                    doc = Document()
                    doc.add(Field("title", title, t1))
                    doc.add(Field("url", url, t1))
                    doc.add(Field("image", image, t1))
                    doc.add(Field("price", price, t1))
                    doc.add(Field("originalprice", '', t1))
                    doc.add(Field("editor", editor, t1))
                    doc.add(Field("rating", rating, t1))
                    doc.add(Field("description", description, t1))
                    doc.add(Field("authors", authors, t1))
                    authors1 = authors.split('\t')
                    for author in authors1:
                        author = author.split('(')[0]
                        author = re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", " ",
                                        author)
                    authors1 = ' '.join(authors1)
                    doc.add(Field("authors1", authors1, t2))
                    doc.add(Field("comments", comments, t1))
                    doc.add(Field("categories", categories, t1))

                    image = re.findall(r'[^\*"/:?\\|<>]', image, re.S)
                    image = "".join(image)
                    doc.add(Field("image1", image, t2))

                    categories = categories.split('\t')
                    categories = ' '.join(categories)

                    seg_title = jieba.cut(title, cut_all=False)
                    title = ' '.join(seg_title)
                    seg_editor = jieba.cut(editor, cut_all=False)
                    editor = ' '.join(seg_editor)
                    seg_categories = jieba.cut(categories, cut_all=False)
                    categories = ' '.join(seg_categories)

                    if title:
                        doc.add(Field("title1", title, t2))
                    else:
                        print "warning: no title in %s" % url
                    if editor:
                        doc.add(Field("editor1", editor, t2))
                    else:
                        print "warning: no editor in %s" % url
                    if categories:
                        doc.add(Field("categories1", categories, t2))
                    else:
                        print "warning: no editor in %s" % url
                    writer.addDocument(doc)
                except Exception, e:
                    print "Failed in indexDocs:", e



if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        IndexFiles("index")
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
