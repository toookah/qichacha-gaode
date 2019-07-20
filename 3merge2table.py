#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 15:30:59 2019

@author: xuyizhou
"""

import pandas as pd
import numpy as np
import re

def step3_process_tel(inputpath,outputpath):
    df = pd.read_excel(inputpath,encoding='utf8')
    list1=df['电话号码']
    list2=df['电话号码（更多号码）']
    
    for i in range(len(list1)):
        if i%50==0:
            print(i)
        if type(list1[i]).__name__=='str':
            if list1[i].find('-')!=-1:
                #print(list1[i])
                test=re.findall('[0-9]{11}；',list1[i])
                list1[i]=";".join(test)
            #print(list1[i].find('-'))    
    for i in range(len(list2)):
        if i%50==0:
            print(i)
        if type(list2[i]).__name__=='str':
            #print('----orin----')
            #print(list2[i])
            test=re.findall('[0-9]{11}；',list2[i])
            list2[i]="".join(test)
            #print('----after----')
            #print(list2[i])
            
            tel=list2[i].split('；')
            for j in range(len(tel)-1):
                df.loc[i,j]=tel[j]
               
    df['电话号码']=list1
    df.rename(columns={'电话号码':'电话1',0:'电话2', 1:'电话3', 2:'电话4',3:'电话5', 4:'电话6', 5:'电话7',6:'电话8', 7:'电话9', 8:'电话9',9:'电话10', 10:'电话11'}, inplace = True)
    df.drop('电话号码（更多号码）',axis=1,inplace=True)
    #删除空白号码的信息
    df.fillna('',inplace=True)
    for i in range(len(df)):
        if (df.loc[i,'电话1']=="")&(df.loc[i,'电话2']==""):
            df.drop(i,inplace=True)
    #print(len(df)) 
    df =df.reset_index(drop=True)  
    #找到电话的索引
    tell_num=0
    for index in df.columns:
        tell_num+=1
        if index=="电话1":
            #print(tell_num)
            break
    #移动电话数据  
    for i in range(len(df)):
        if (df.loc[i,'电话1']==""):
            for j in range(len(df.columns)-tell_num):
                df.iloc[i,tell_num-1+j]=df.iloc[i,tell_num+j]
          
            
    df=df.drop('省份',axis=1)    
    df=df.drop('城市',axis=1)  
    df=df.drop('统一社会信用代码',axis=1)  
    df=df.drop('企业类型',axis=1)      
    df=df.drop('成立日期',axis=1)    
    df=df.drop('经营范围',axis=1)  
    df=df.drop('网址',axis=1)  
    df.to_csv(outputpath,encoding='utf_8_sig',index=None)


filename='名称'
dirname=filename+'/'
step3_process_tel(dirname+filename+'_cut.xls',dirname+'middle.csv')

input_path=dirname+filename+'_cut.csv'   
df = pd.read_csv(input_path,encoding='utf8')
df.columns=['newname','id','企业名称','省份','城市','区','具体地址']
df2 = pd.read_csv(dirname+'middle.csv',encoding='utf8')
result1 = pd.merge(df2,df,on='newname',how='left')
#print(result1.columns)
result1.drop_duplicates('newname','first', inplace=True)
#print(result1)
result1=result1.fillna('')
result2=result1[result1['省份']!=""]
#删除没有地址
result2=result2.drop('id',axis=1)
result2 = result2.astype(np.object)
result3=result2[result2!='[]']
result3=result3.dropna()
result3['地址']=result3['省份']+result3['城市']+result3['区']+result3['具体地址']
result3=result3.drop('省份',axis=1)
result3=result3.drop('城市',axis=1)
result3=result3.drop('区',axis=1)
result3=result3.drop('具体地址',axis=1)
#两个表相减

df2=df2.append(result3)
df2=df2.append(result3)
df_outofgaode=df2.drop_duplicates('newname',keep=False)
result3.to_excel(dirname+filename+'_res1_gaode'+str(len(result3))+'.xls',encoding='utf_8_sig',index=None)
df_outofgaode.to_excel(dirname+'res2_outofgaode.xls',encoding='utf_8_sig',index=None)
#给客户
start=filename.find('2')
result3.drop('newname',axis=1,inplace=True)
result3.drop('企业名称_y',axis=1,inplace=True)
result3_name_x=result3['企业名称_x']
result3.drop('企业名称_x',axis=1,inplace=True)
result3.insert(0,'企业名称',result3_name_x)
result3.to_excel(dirname+filename[0:start]+str(len(result3))+'.xls',encoding='utf_8_sig',index=None)
