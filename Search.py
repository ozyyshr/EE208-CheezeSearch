# -*- coding: UTF-8 -*-
#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene

from bs4 import BeautifulSoup
import urllib2

import re
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
import jieba
reload(sys)
sys.setdefaultencoding('utf8')


def run(searcher, analyzer):
    while True:
        print
        print "Hit enter with no input to quit."
        command = raw_input("Query:")
        command = unicode(command, 'utf-8')

        if command == '':
            return

        print
        print "Searching for:", command

        command = re.findall(r'[^\*"/:?\\|<>]', command, re.S)
        command = "".join(command)
        print command


        querys = BooleanQuery()
        query_title = QueryParser(Version.LUCENE_CURRENT, "title1",
                            analyzer).parse(command)
        query_author = QueryParser(Version.LUCENE_CURRENT, "authors1",
                                   analyzer).parse(command)
        query_editor = QueryParser(Version.LUCENE_CURRENT, "editor",
                                  analyzer).parse(command)
        query_category = QueryParser(Version.LUCENE_CURRENT, "categories1",
                                   analyzer).parse(command)
        query_image = QueryParser(Version.LUCENE_CURRENT, "image1",
                                     analyzer).parse(command)

        querys.add(query_title, BooleanClause.Occur.SHOULD)
        querys.add(query_author, BooleanClause.Occur.SHOULD)
        querys.add(query_editor, BooleanClause.Occur.SHOULD)
        querys.add(query_category, BooleanClause.Occur.SHOULD)
        querys.add(query_image, BooleanClause.Occur.SHOULD)

        scoreDocs = searcher.search(querys, 50).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            print '------------------------------------------------------------------'
            print 'title:', doc.get("title"), 'url:', doc.get("url"), 'image:', doc.get("image"), 'price:', doc.get("price"),'originalprice:', doc.get("originalprice"), 'editor:', doc.get("editor"),\
                'rating:', doc.get("rating"), 'description:', doc.get("description"), 'authors:', doc.get("authors"), 'comments:', doc.get("comments"), 'categories:', doc.get("categories"), 'score:', scoreDoc.score
            # print 'explain:', searcher.explain(query, scoreDoc.doc)





if __name__ == '__main__':
    STORE_DIR = "index"
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)

    run(searcher, analyzer)
    del searcher
