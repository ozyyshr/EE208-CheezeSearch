# CheezeSearch

### 1.网站定位

该网站通过图书关键字进行文本搜索以及图书相关图片进行图片搜索，对搜索结果依据不同的属性进行排序，并针对用户的搜索内容作出相关的推荐。

### 2.开发环境

- VirtualBox上的Linux系统

- python 2.7 编译器为pycharm

- **Lucene**：是一套用于[全文检索](https://baike.baidu.com/item/全文检索/8028630)和搜寻的开源程式库，目的是为软件开发人员提供一个简单易用的工具包，以方便的在目标系统中实现全文检索的功能，或者是以此为基础建立起完整的全文检索引擎。

- python中重要的库：

  - requests: 常用的用于http请求的模块
  - re: python中处理正则表达式的库
  - urllib：一个功能强大,条理清晰,用于HTTP客户端的Python库
  - BeautifulSoup：一个可以从HTML或XML文件中提取数据的Python库
  - jieba：分词器
  - web：构建网页的框架
  - scipy：专门用于科学计算的一个常用的库
  - numpy：支持矩阵向量等多维数据运算的python模块


### 3.文件目录结构

```
├─book
├─files             //亚马逊图书网的图书信息，每本书放在一个txt文件中
├─index             //文本搜索的索引
├─messages_books    //当当网的图书信息，每本书放在一个txt文件中
├─IndexFiles.py     //索引建立
├─crawler.py        //爬取亚马逊网的图书信息
├─dangdang_1.py
├─dangdang_2.py      //爬取当当网的图书信息
├─generate_image_feature_ORB.py
├─pic_search
│  ├─big_index2.py
│  └─index
├─static            //存放css、js、font等样式的静态文件
│  ├─css
│  ├─css1
│  ├─css2
│  │  ├─bootstrap
│  │  │  └─css
│  │  ├─font-awesome
│  │  │  ├─css
│  │  │  └─fonts
│  │  ├─footer
│  │  ├─header
│  │  └─themecss
│  ├─fonts
│  ├─fonts1
│  ├─images
│  ├─images1
│  ├─js
│  ├─js1
│  └─js2
│      ├─countdown
│      ├─datetimepicker
│      ├─dcjqaccordion
│      ├─jquery-ui
│      ├─minicolors
│      ├─modernizr
│      ├─owl-carousel
│      ├─slick-slider
│      ├─themejs
│      └─unveil
├─templates             //网页模板
├─code.py               //启动文件，连接前后端
├─Search.py             //文本搜索功能
├─Search_img.py
├─Search_image.py
├─Search_filter.py      //搜索结果过滤功能
├─Search_filter.html    //过滤后的搜索结果呈现模板
├─image_data2.mat
├─image_data3.mat
    …………
├─image_data59.mat
├─image_data62.mat
├─image_press.mat
```

### 4.重要程序的具体介绍

- crawler.py

  - 库调用：

    ```python
    import sys
    import importlib
    import requests
    importlib.reload(sys)
    import time
    import urllib.error
    import requests
    import json
    import re
    import urllib.request
    import urllib
    import re
    import random
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    from urllib.parse import urlencode
    from urllib.parse import quote
    from urllib import parse
    ```

  - 函数简单原理：

    1.parseAmazon:使用bs4读取网页爬取信息，一并存入数组，然后写入txt文件备用。
    2.write_documents:写入文件，生成每本图书的信息txt
    3.get_title:辅助函数，用于提取最简书名，便于修改url搜索
    4.parseComments,parsePrice,parseEditor,parseAuthor,parseDescription,parseCategory:在chrome中查看具体div位置以后，使用bs4爬取相关信息
    5.randHeader:随机提取agent调换header，减少被原网站防爬
    6.get_page:利用randHeader随机得到agent，再添加cookie信息防止进入验证码界面，将cookie和header用session绑定，并随机使用proxy_list当中的高匿ip地址，减少被原网站防爬
    7.main:调用以上函数，完成爬虫

- IndexFiles.py

  - 库调用：

    ```python
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
    import urllib2
    from bs4 import BeautifulSoup
    reload(sys)
    sys.setdefaultencoding('utf-8')
    ```

  - 函数简单原理：

    1.Ticker:计时
    2.IndexFiles:调用lucene中的分词器，打开准备好的txt文件，逐行读取信息建立索引，分为可以检索的t2 Field和仅限存储的t1 Field

- code.py

  - 库调用：

    ```python
    INDEX_DIR = "IndexFiles.index"
    import lucene
    import re
    import Search
    import Search_img
    import Search_image
    import Search_filter
    import web
    from web import form
    import cv2
    import scipy.io as scio
    import numpy as np
    import os, lucene
    import threading
    from org.apache.lucene.search.highlight import TokenSources
    from org.apache.lucene.search.highlight import QueryScorer
    from org.apache.lucene.search.highlight import SimpleHTMLFormatter
    from org.apache.lucene.search.highlight import Highlighter
    from org.apache.lucene.search.highlight import InvalidTokenOffsetsException
    from org.apache.lucene.search.highlight import SimpleSpanFragmenter
    from org.apache.lucene.search.highlight import SimpleFragmenter
    import sys
    from web import form
    import io
    from java.io import File
    from org.apache.lucene.analysis.core import SimpleAnalyzer
    from org.apache.lucene.index import DirectoryReader
    from org.apache.lucene.queryparser.classic import QueryParser
    from org.apache.lucene.queryparser.classic import MultiFieldQueryParser
    from org.apache.lucene.store import SimpleFSDirectory
    from org.apache.lucene.search import IndexSearcher
    from org.apache.lucene.util import Version
    import jieba
    from lucene import *
    from org.apache.lucene.search import BooleanClause
    from org.apache.lucene.search import  TermQuery
    from org.apache.lucene.index import Term
    ```

  - 函数简单原理：

    1.index:调用index.html呈现前端
    2.s:调用result.html呈现结果
    3.f:用于过滤功能，对应不同的Search分词文件

- search_img.py

  - 库调用：

    ```python
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
    reload(sys)
    sys.setdefaultencoding('utf8')
    ```

  - 函数简单原理：

    1.run:调用lucene分词器，在index中检索输入关键字的信息，根据前端需要按照规整格式存入数组中，同时进行相关排序，返回给code.py
    2.run_rel:返回值比run简单，原理一致，用于推荐同一作者的著作
    3.Search_filter中的run:原理一致，将lucene中parser的SHOULD改为MUST，进行两个关键字的过滤工作

### 5.程序运行方法

运行文件中的code.py文件，并打开console中提供的localhost网址。按照网页中的提示输入搜索条目。