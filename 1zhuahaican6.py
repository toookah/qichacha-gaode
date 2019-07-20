#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 15:09:20 2019

@author: xuyizhou
"""

#高德地图POI信息抓取,青岛别墅  ok

from urllib.parse import quote
from urllib import request
import json
import xlwt
import pandas as pd
import os
#TODO 替换为上面申请的密钥

#   5c2afa76a2db108223752ea2cfdbd50b
#----------parameters0417-------------
poi_search_url = "http://restapi.amap.com/v3/place/text"
poi_boundary_url = "https://ditu.amap.com/detail/get/detail"
#from transCoordinateSystem import gcj02_to_wgs84
filename='青岛口腔'
df_2=pd.read_excel(filename+'.xls',encoding='utf8')
df_2.fillna('',inplace=True)
# sharedata = ['青岛众合摆渡广告有限公司','青岛麦迪绅集团有限公司']
classes = list(df_2["企业名称"])
pnames = list(df_2["省份"])
citynames = list(df_2["城市"])

#print("classes--------")
#print(classes)

#TODO cityname为需要爬取的POI所属的城市名，nanning_areas为城市下面的所有区，classes为多个分类名集合. (中文名或者代码都可以，代码详见高德地图的POI分类编码表)

#cityname = '全国'#xyz
# nanning_areas = ['市南区','市北区','李沧区','崂山区']


# classes = ['青岛众合摆渡广告有限公司','青岛麦迪绅集团有限公司','青岛市旅游规划建筑设计研究院']
# print(type(classes))
# classes = ['汇和弘毅投资控股有限公司', '零壹私募证券投资基金管理(广州)有限责任公司', '秀实投资管理集团有限公司', '中建城投产业基金有限公司', '中建城投产业新城投资有限公司', '领高控股有限公司', '山东国安证券服务股份有限公司', '国世投资基金管理(北京)有限公司', '财投投资有限公司']
# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords, i)
        #print(result)
        result = json.loads(result)  # 将字符串转换为json
        #print(result)
        if result['count'] == '0':
            #print("result['count'] == '0'")
            break
        hand(poilist, result)
        i = i + 1
        if i>1:
            break
    #print("poilist--------")
    #print(poilist)
    return poilist


# 数据写入excel
def write_to_excel(poilist, cityname,filename):
    result =[]
    fn = filename+'.csv'
    for i in range(len(poilist)):
        name = poilist[i]['name']
        # tel = poilist[i]['tel']
        pname = poilist[i]['pname']
        cityname = poilist[i]['cityname']
        adname=poilist[i]['adname']
        addname = poilist[i]['address']
        result.append([name, pname,cityname,adname,addname])
        if abs(i+1-len(poilist))<0.01:
        # if i == len(poilist):
        # print([name,addname])
        #     print(result)
            df = pd.DataFrame( result)
            if os.path.exists(fn):
                df.to_csv(fn, mode='a', header=None, encoding='utf_8_sig')
            else:
                df.to_csv(fn, encoding='utf_8_sig')

            # df = pd.DataFrame(result)
            # df.to_excel('青岛别墅.xls')



# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])


# 单页获取pois
def getpoi_page(cityname, keywords, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    #types是类，keywords是关键字
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data


# for clas in sharedata.values:
for i in range(len(classes)):
    amap_web_key = '0864776b66cb3ca0f259a2a737bce24d'
    if i%50==0:
        print(i)
    if i>=2000:
        amap_web_key = '0d0f94348a01cedc7d1c96e9f871894f'
    if i>=4000:
        amap_web_key = 'dee4a77852137fdd345d83fa480f7fd1'
    clas=classes[i]
    pname=pnames[i]
    cityname=citynames[i]
    
    if cityname=="":
        cityname_for_search=pname
    else:
        cityname_for_search=cityname
    #cityname_for_search="全国"
    #print("要查询的名称:",clas)
    #print("要查询的名称:",cityname_for_search)

    classes_all_pois = []
    # for area in nanning_areas:
    pois_area = getpois(cityname_for_search,clas)
    # print('当前城区：' + str(area) + ', 分类：' + str(clas) + ", 总的有" + str(len(pois_area)) + "条数据")
    classes_all_pois.extend(pois_area)
    # print("所有城区的数据汇总，总数为：" + str(len(classes_all_pois)))

    write_to_excel(classes_all_pois, cityname_for_search,filename)

    # print('================分类：'  + str(clas) + "写入成功")
