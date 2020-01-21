# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
from PIL import Image
import cStringIO
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
import cv2
import scipy.io as scio
import numpy as np

maximum_features=618
scale_factor=1.2
data_file = 'image_data1.mat'
#data_file = 'image_data2.mat'
#data_file = 'image_data3.mat'
knn_match_num=20

def get_image_path():
    root='messages_books'
    #root='book'
    #root='files'
    files=os.listdir(root)
    img_list=[]
    for file in files:
        f=open(root+'/'+file,'r')
        img=f.readlines()[2].strip()
        img_list.append(img)
    return img_list

def generate_image_feature(img_list):
    img_dict={}
    for img in img_list:
        print img
        file = cStringIO.StringIO(urllib2.urlopen(img).read())
        i = Image.open(file)
        image = np.array(i,dtype='uint8')
        orb=cv2.ORB_create(maximum_features,scale_factor)
        kp,feature=orb.detectAndCompute(image,None)
        img_dict[img]=feature
    scio.savemat(data_file, img_dict)

def generate_search_feature(img_path):
    file = cStringIO.StringIO(urllib2.urlopen(img_path).read())
    i = Image.open(file)
    image = np.array(i, dtype='uint8')
    orb = cv2.ORB_create(maximum_features, scale_factor)
    kp, feature = orb.detectAndCompute(image, None)
    return feature

def knn_match(search_feature,feature):
    feature=np.array(feature,dtype='uint8')
    bf_matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf_matcher.knnMatch(search_feature, trainDescriptors=feature, k=2)
    good_matches = [m for (m, n) in matches if m.distance < 0.75 * n.distance]
    return len(good_matches)

def image_search(image_path,img_list):
    data = scio.loadmat(data_file)
    print data
    search_feature=generate_search_feature(image_path)
    match_results=[]
    for img in img_list:
        feature=data[img]
        match_num=knn_match(search_feature,feature)
        if match_num > knn_match_num:
            match_results.append((img,match_num))
    return match_results


img_list=get_image_path()
generate_image_feature(img_list)
#u='http://img3m3.ddimg.cn/79/21/25220923-1_b_3.jpg'
#print image_search(u,img_list[:10])



