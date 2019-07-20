#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import os
path='resultmerge/'
df_main = pd.DataFrame()
for file in os.listdir(path):  
    print(file)
    df=pd.read_excel(path+file,encoding='utf8')
    res = pd.concat([df_main,df], axis=0, ignore_index=True)
    df_main=res
    print(len(df_main))
    print(df_main.columns)

df_main.drop_duplicates(keep='first',inplace=True)
print(len(df_main))
df_main.to_excel(path+'result'+str(len(df_main))+'.xls', encoding='utf_8_sig',index=None)  
    