import web
import cv2
import scipy.io as scio
import numpy as np
import os, lucene
import threading
import re
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

urls = (
    '/', 'Upload',
    '/show','result'
)

render = web.template.render('templates_book', cache=False)

maximum_features=618
scale_factor=1.2
knn_match_num=100
varLock = threading.Lock()
match_results = []
threads=[]

def get_image_path():
    root='messages_books'
    files=os.listdir(root)
    img_list=[]
    for file in files:
        f=open(root+'/'+file,'r')
        img=f.readlines()[2].strip()
        img_list.append(img)
    return img_list
img_list=get_image_path()

def Quicksort(arr, start, end):
    if start >= end:
        return
    low = start
    mid = arr[start]
    high = end
    while low < high:
        while low < high and mid[1] >= arr[high][1]:
            high -= 1
        arr[low] = arr[high]
        while low < high and mid[1] < arr[low][1]:
            low += 1
        arr[high] = arr[low]
    arr[low] = mid
    Quicksort(arr, start, low - 1)
    Quicksort(arr, low + 1, end)

class Upload:
    def GET(self):
        return render.b1()
    def POST(self):
        x = web.input(myfile={})
        y = web.input(mypress={})
        filedir = './' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filename="thisismy.file" # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
        if 'mypress' in y:
            pressname='thisispress.file'
            fout = open(filedir +'/'+ pressname,'w')
            fout.write(y.mypress.file.read())
            fout.close()
        raise web.seeother('/show')

def knn_match(search_feature,feature):
    feature=np.array(feature,dtype='uint8')
    bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf_matcher.knnMatch(search_feature, trainDescriptors=feature, k=2)
    good_matches = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
    return len(good_matches)

def search_img(match_result,vm_env,searcher,analyzer):
    results = list()
    for match in match_result:
        aha=re.findall(r'[^\*"/:?\\|<>]',match[0],re.S)
        aha="".join(aha)
        query = TermQuery(Term('image1', aha, ))
        scoreDocs = searcher.search(query, 1).scoreDocs
        for i, scoreDoc in enumerate(scoreDocs):
            result = list()
            doc = searcher.doc(scoreDoc.doc)
            result.append(doc.get("title"))
            result.append(doc.get("url"))
            result.append(doc.get("image"))
            result.append(doc.get("price"))
            result.append(doc.get("originalprice"))
            result.append(doc.get("originalprice"))
            result.append(doc.get("editor"))
            result.append(doc.get("rating"))
            result.append(doc.get("description"))
            result.append(doc.get("authors"))
            result.append(doc.get("comments"))
            result.append(doc.get("categories"))
            results.append(result)
    return results,len(results)

def image_search(file_name,search_feature):
    data = scio.loadmat(file_name)
    for img in data:
        if img!='__version__' and img!='__header__' and img!='__globals__':
            feature = data[img]
            match_num = knn_match(search_feature, feature)
            if match_num > knn_match_num:
                if varLock.acquire():
                    match_results.append((img, match_num))
                    varLock.release()
def search_press(match_result,vm_env,searcher,analyzer):
    results = list()
    for match in match_result:
        aha=re.findall(r'[^\*"/:?\\|<>]',match[0],re.S)
        aha="".join(aha)
        print aha
        query = TermQuery(Term('editor',aha,))
        scoreDocs = searcher.search(query, 1).scoreDocs
        for i, scoreDoc in enumerate(scoreDocs):
            result = list()
            doc = searcher.doc(scoreDoc.doc)
            result.append(doc.get("title"))
            result.append(doc.get("url"))
            result.append(doc.get("image"))
            result.append(doc.get("price"))
            result.append(doc.get("originalprice"))
            result.append(doc.get("originalprice"))
            result.append(doc.get("editor"))
            result.append(doc.get("rating"))
            result.append(doc.get("description"))
            result.append(doc.get("authors"))
            result.append(doc.get("comments"))
            result.append(doc.get("categories"))
            print result
            results.append(result)
    return results,len(results)
class result:
    def GET(self):
        res=[]
        res_press=[]
        if os.path.exists("thisismy.file"):
            image=cv2.imread("thisismy.file")
            orb = cv2.ORB_create(maximum_features, scale_factor)
            kp, search_feature = orb.detectAndCompute(image, None)
            global match_results,threads
            match_results = []
            threads=[]
            for i in ['2','3','4','5','6','7','8','10','11','49','50','51','52','53','54','55','56','57','58','59','62']:
                file_name='image_data'+i+'.mat'
                t = threading.Thread(target=image_search,args=(file_name,search_feature,))
                t.setDaemon(True)
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            Quicksort(match_results,0,len(match_results)-1)
            vm_env = lucene.getVMEnv()
            vm_env.attachCurrentThread()
            STORE_DIR = "index"
            directory = SimpleFSDirectory(File(STORE_DIR))
            searcher = IndexSearcher(DirectoryReader.open(directory))
            analyzer = SimpleAnalyzer(Version.LUCENE_CURRENT)
            res,len_res=search_img(match_results,vm_env,searcher,analyzer)
            os.remove("thisismy.file")
        if os.path.exists("thisispress.file"):
            image=cv2.imread("thisispress.file")
            orb = cv2.ORB_create(maximum_features, scale_factor)
            kp, search_feature = orb.detectAndCompute(image, None)
            data = scio.loadmat('image_press.mat')
            match_results = []
            for img in data.keys():
                if img != '__version__' and img != '__header__' and img != '__globals__':
                    feature = data[img]
                    match_num = knn_match(search_feature, feature)
                    if match_num > knn_match_num:
                        match_results.append((img, match_num))
            Quicksort(match_results,0,len(match_results)-1)
            vm_env = lucene.getVMEnv()
            vm_env.attachCurrentThread()
            STORE_DIR = "index"
            directory = SimpleFSDirectory(File(STORE_DIR))
            searcher = IndexSearcher(DirectoryReader.open(directory))
            analyzer = SimpleAnalyzer(Version.LUCENE_CURRENT)
            res_press,len_press=search_press(match_results,vm_env,searcher,analyzer)
            print res_press
            os.remove("thisispress.file")
        return render.b2(res,res_press)

if __name__ == "__main__":
    vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    app = web.application(urls, globals())
    app.run()