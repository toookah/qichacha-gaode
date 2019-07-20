#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 10:38:44 2019
删除一些固定名词
@author: xuyizhou
"""

import jieba.posseg as pseg
import pandas as pd
import numpy as np


def cutname(inputpath,name_of_col,outputpath,typename):
    if typename==".csv":
        df = pd.read_csv(inputpath,encoding='utf8')
    else:
        df = pd.read_excel(inputpath,encoding='utf8')
    names=df[name_of_col]
    #names_small=names[1:10]
    i=1
    new_words=[]
    for name in names:#names_small
        if i%500==0:
            print(i)
        i=i+1
        #seg_list = jieba.cut(name) #默认是精确模式
        #print (", ".join(seg_list))
        words =pseg.cut(name)
        new_word=""
        for w in words:
            #print(w.word,w.flag)
            dicta=['管理','餐饮','配送','服务','中心','口腔','门诊部','口腔诊所','口腔医院','分公司','婚纱','摄影','有限公司','有限责任','公司','青岛','青岛市']
            if (w.flag!="x")&(w.word not in dicta):
                new_word+=w.word
        #print(new_word)
        new_words.append(new_word)
        #print('----------------')
    df.insert(0,'newname',new_words)
    if typename==".csv":
        df.to_csv(outputpath,encoding='utf_8_sig',index=None)
    else:
        df.to_excel(outputpath,encoding='utf_8_sig',index=None)
    

filename='名称'
typename='.csv'
inputpath=filename+'/'+filename+typename
name_of_col='0'
outputpath=filename+'/'+filename+'_cut'+typename
cutname(inputpath,name_of_col,outputpath,typename)
typename='.xls'
inputpath=filename+'/'+filename+typename
name_of_col='企业名称'
outputpath=filename+'/'+filename+'_cut'+typename
cutname(inputpath,name_of_col,outputpath,typename)

