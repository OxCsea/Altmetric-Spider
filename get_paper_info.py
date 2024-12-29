# -*- coding: utf-8 -*-
"""
根据doi爬取论文基本信息
"""

import requests
import re
from fake_useragent import UserAgent
import pandas as pd
import time
import csv
import math

def get_header():
    ua = UserAgent(verify_ssl=False)
    return {'User-Agent': ua.random}


def get_paperInfo(filepath):
    '''
    1 - DOI
    3 - Article Name
    7 - Times Cited
    11 -Publication Date
    '''
    info_df =  pd.read_csv(filepath,dtype=str,usecols=[0])
    print('finish info_df')
    # 可选择是否导出csv
    # info_df.to_csv('./info_df.csv',index = False,header=True)
    return info_df


   
def get_details(info_df,path1,path2):
    """
    info_df 含有所需信息的dataframe
    path1 数据保存路径1
    path2 数据保存路径2
    采用双重导出的方式 避免因爬取过程中bug而出现的大量数据丢失
    如果运行正确 path1内容=path2内容
    """
    detail_url = []
    AAS =[]
    requests.adapters.DEFAULT_RETRIES = 5
    doi = info_df['doi']
    """
    根据需要补充信息，这里只爬取doi detail_url, aas
    # title = info_df['Article Name']
    # cited = info_df['Times Cited']
    # date = info_df['Publication Date']
    """
    doilen = len(doi)
    with open(path1,'a+') as f:
        writer = csv.writer(f)
        writer.writerow(["doi","detail_url","aas"]) 
    #i用于遍历
    i = 0
    fail_cnt = 0
    while(i < doilen):
        baseUrl = 'http://api.altmetric.com/v1/doi/'+str(doi[i])
        try:
            if (fail_cnt > 2):
                i += 1
                fail_cnt = 0
                print(baseUrl+'--- fail next')
                continue
            r = requests.get(baseUrl, headers=get_header())
            #cont -- content
            cont = r.text
            fail_cnt = 0
            exist = re.findall(r'Not Found',cont)
            if exist == []:
                pdetail = r'details_url":"(.*?)"'
                detail = re.findall(pdetail,cont)
                paas = r'score":(.*?),'
                aas = re.findall(paas,cont)
                detail_url.extend(detail)
                AAS.extend(aas)
                # time.sleep(300)
            else:
                # 如果没有这个就可能出现doi和url不同长度的情况
                detail_url.append(' ')
                AAS.append(' ')
                print(str(doi[i])+'     is null')
            cont_index = [doi[i],detail_url[i],AAS[i]]
            if(i%10 == 0):
                print(str(i))
            with open(path1,'a+') as f:
                writer = csv.writer(f)
                writer.writerow(cont_index)           
            i += 1
        except:
            print("Connection refused by the server..")
            fail_cnt += 1
            time.sleep(5)
            continue
   
    detail_urllen = len(detail_url)
    AAS_len = len(AAS)
    minlen = min(doilen,detail_urllen,AAS_len)
    detail_info = {
        "doi":doi[:minlen],
        "detail_url":detail_url[:minlen],
        "aas":AAS[:minlen]
        }
    print('len of doi' + str(len(doi)))
    print('len of detail_url' + str(len(detail_url)))
    print('len of aas' + str(len(AAS)))
    details = pd.DataFrame(detail_info)
    details.to_csv(path2,index = False,header=True)
    print('finish details')
    return details

if __name__  == '__main__':
    filepath = 'paper_doi.csv'
    info = get_paperInfo(filepath)
    path1 = 'paper_info.csv'
    path2 = 'paper_info_bak.csv'
    get_details(info,path1,path2)
    print('finish all process')    
