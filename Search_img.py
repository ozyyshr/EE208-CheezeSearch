# -*- coding: UTF-8 -*-
#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene

from bs4 import BeautifulSoup
import urllib2

import re
import copy
import math
from java.io import File
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.analysis.core import StopAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause

import sys
reload(sys)
sys.setdefaultencoding('utf8')


"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""


def run(a, pageindex=1, pagesize=10):
    vm_env=lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index"
    print 'lucene', lucene.VERSION
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)

    a = re.findall(r'[^\*"/:?\\|<>]', a, re.S)
    a = "".join(a)

    querys = BooleanQuery()
    query_title = QueryParser(Version.LUCENE_CURRENT, "title1",
                              analyzer).parse(a)
    query_author = QueryParser(Version.LUCENE_CURRENT, "authors1",
                               analyzer).parse(a)
    query_editor = QueryParser(Version.LUCENE_CURRENT, "editor1",
                               analyzer).parse(a)
    query_category = QueryParser(Version.LUCENE_CURRENT, "categories1",
                                 analyzer).parse(a)
    query_image = QueryParser(Version.LUCENE_CURRENT, "image1",
                              analyzer).parse(a)

    querys.add(query_title, BooleanClause.Occur.SHOULD)
    querys.add(query_author, BooleanClause.Occur.SHOULD)
    querys.add(query_editor, BooleanClause.Occur.SHOULD)
    querys.add(query_category, BooleanClause.Occur.SHOULD)
    querys.add(query_image, BooleanClause.Occur.SHOULD)
    scoreDocs = searcher.search(querys, 50).scoreDocs

    result = []

    start = (pageindex - 1) * pagesize
    end = start + pagesize

    for scoreDoc in scoreDocs[start:end + 10]:
        doc = searcher.doc(scoreDoc.doc)
        sub = []
        sub.append(doc.get("title"))#0
        sub.append(doc.get("url"))#1
        sub.append(doc.get("image"))#2
        price = doc.get("price").strip()
        if price:
            price = float(price)
        else:
            price = 0
        sub.append(price)#3
        editor = doc.get("editor")
        eurl = "http://0.0.0.0:8080/filter?keyword="+editor+'+'+a

        sub.append([editor, eurl])#4
        rating = doc.get("rating").strip()

        if rating == "None" or not rating:
            rating = 0
        else:
            rating = float(rating)
        sub.append(rating)#5
        sub.append(doc.get("description"))#6
        sub.append(doc.get("authors"))#7

        comments = doc.get("comments")
        comments = comments.split('\t')
        if len(comments[0]) == 2:
            comments = ["Not Commented Yet"]

        sub.append(comments[:4])#8
        sub.append(doc.get("categories"))#9

        rstar = math.ceil(rating/20)
        sub.append(rstar)#10

        result.append(sub)

    del searcher
    resultprice = copy.deepcopy(result)
    resultrating = copy.deepcopy(result)
    resultprice = sorted(resultprice, key=lambda x: x[3])
    cnt = 1
    for sub in resultprice:
        sub.append(cnt)#11
        cnt += 1
    cnt = 1
    resultrating = sorted(resultrating, key=lambda x: -x[5])
    for sub in resultrating:
        sub.append(cnt)#11
        cnt += 1
    return result, resultprice, resultrating, len(scoreDocs)

def run_rel(a):
    vm_env=lucene.getVMEnv()
    vm_env.attachCurrentThread()
    STORE_DIR = "index"
    print 'lucene', lucene.VERSION
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)

    a = re.findall(r'[^\*"/:?\\|<>]', a, re.S)
    a = "".join(a)


    querys = BooleanQuery()
    query_title = QueryParser(Version.LUCENE_CURRENT, "title1",
                              analyzer).parse(a)
    query_author = QueryParser(Version.LUCENE_CURRENT, "authors1",
                               analyzer).parse(a)
    query_editor = QueryParser(Version.LUCENE_CURRENT, "editor1",
                               analyzer).parse(a)
    query_category = QueryParser(Version.LUCENE_CURRENT, "categories1",
                                 analyzer).parse(a)
    query_image = QueryParser(Version.LUCENE_CURRENT, "image1",
                              analyzer).parse(a)

    querys.add(query_title, BooleanClause.Occur.SHOULD)
    querys.add(query_author, BooleanClause.Occur.SHOULD)
    querys.add(query_editor, BooleanClause.Occur.SHOULD)
    querys.add(query_category, BooleanClause.Occur.SHOULD)
    querys.add(query_image, BooleanClause.Occur.SHOULD)
    scoreDocs = searcher.search(querys, 50).scoreDocs

    result = []

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        sub = []
        sub.append(doc.get("title"))#0
        sub.append(doc.get("url"))#1
        sub.append(doc.get("image"))#2
        price = doc.get("price").strip()
        if price:
            price = float(price)
        else:
            price = 0
        sub.append(price)#3
        sub.append(doc.get("originalprice"))#4
        rating = doc.get("rating").strip()
        if rating == "None" or not rating:
            rating = 0
        else:
            rating = float(rating)
        sub.append(rating)#5
        sub.append(doc.get("description"))#6
        sub.append(doc.get("authors"))#7

        comments = doc.get("comments")
        comments = comments.split('\t')
        comments = comments[:4]

        sub.append(comments)#8
        sub.append(doc.get("categories"))#9

        rstar = math.ceil(rating / 20)
        sub.append(rstar)  # 10

        result.append(sub)
        if len(result) == 8:
            break
    del searcher
    return result



