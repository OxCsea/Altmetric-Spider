# -*- coding: utf-8 -*-
"""
根据论文基本信息中的url爬取altmetrics信息
"""

import requests
import re
from fake_useragent import UserAgent
import pandas as pd
import csv
# from getDetails import get_paperInfo,get_details
import time

def get_header():
    ua = UserAgent(verify_ssl=False)
    return {'User-Agent': ua.random}


def get_detailInfo(filepath):
    '''
    1 - DOI
    3 - Article Name
    7 - Times Cited
    11 -Publication Date
    '''
    detail_df =  pd.read_csv(filepath,dtype=str,usecols=[4]).iloc[:,:]
    print('finish detail_df')
    return detail_df

def getAlt(details,outpath):
    index = 0
    urllist = details.iloc[:,1]
    urllist_len = len(urllist)
    doilist = details.iloc[:,0]
    news = []
    blogs = []
    policy = []
    twitter = []
    patent = []
    weibo = []
    facebook = []
    wikipedia = []
    googleplus = []
    reddit = []
    video = []
    dimensions_citation = []
    mendeley = []
    citeulike = []
    with open(outpath,'a+') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(["doi","news", "blogs", "policy","twitter", "patent", \
                                    "weibo","facebook","wikipedia", "googleplus","reddit","video",\
                                    "dimensions_citation","mendeley", \
                                    "citeulike"])
    failcnt = 0
    while (index < urllist_len):
        url = urllist[index]
        df = pd.DataFrame(columns = ["news", "blogs", "policy","twitter", "patent", \
                                    "weibo","facebook","wikipedia", "googleplus","reddit","video",\
                                    "dimensions_citation","mendeley", \
                                    "citeulike"])
        if (failcnt >= 3):
            index += 1
            failcnt = 0
            print(url+'------fail  = 3, next')
            continue
        try:
            if url == " ":
                cont_index = [doilist[index],0,0,0,0, \
                            0,0,0,0,0, \
                            0, 0,0,0, \
                            0]
                failcnt = 0
            else:
                r = requests.get(url, headers=get_header())
                r.encoding = r.apparent_encoding
                cont = r.text
                failcnt = 0
                ptag = r'<dt style=.*?>(.*?)</dt>'
                tags = re.findall(ptag,cont)
                pnum = r'<strong>(.*?)</strong>'
                taglen = len(tags)
                nums = re.findall(pnum,cont)[:taglen]
                nums = list(map(int, nums))
                alt = {
                        "tags":tags,
                        "nums":nums
                        }
                alt = pd.DataFrame(alt)
                columns = df.columns.values.tolist()
                for clm in columns:
                    ind = alt[(alt.tags == clm)].index.tolist()
                    ind = ind[0] if len(ind)>0 else -1
                    eval(clm).append(0 if ind == -1 else alt.iat[ind,1])

                cont_index = [doilist[index],news[index],blogs[index],policy[index],twitter[index], \
                                patent[index],weibo[index],facebook[index],wikipedia[index],googleplus[index], \
                                reddit[index], video[index],dimensions_citation[index],mendeley[index], \
                                citeulike[index]]
            with open(outpath,'a+') as csvf:
                writer = csv.writer(csvf)
                writer.writerow(cont_index)
            index += 1
        except:
           print("Connection refused")
           failcnt += 1
           time.sleep(5)
           continue
    print("finish all!")
#    return res


if __name__ == '__main__':
    # 含detail url的文件
    path = 'paper_info.csv'
    details = pd.read_csv(path,dtype=str)
    #结果保存的路径
    outpath = 'altmetrics.csv'
    getAlt(details,outpath)
    
