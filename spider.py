# -*- coding: UTF-8 -*-
import os

import requests
import json
import math
import re

base_url="https://hanime.tv/api/v3/"
pageapi="browse/trending?"
detailapi="hentai-videos/"
radomapi="random"
tagapi="browse/hentai-tags/"
pagenum=1
headers={
        'Host': 'hanime.tv',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Accept': 'application/json;charset=utf-8',
        # 'Accept-Language': 'EN',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Referer': 'https://hanime.tv/browse/trending',
        'X-Directive': 'api'
        # # 'Cookie': '__cfduid=d222a4fd06ba7e080091dab908d9d61571531782705; _ga=GA1.2.1971138364.1531782711; _gid=GA1.2.1726613045.1531782711; ld=1; vreso=720P',
        # 'Connection': 'keep - alive',
        # 'Pragma': 'no-cache',
        # 'Cache-Control': 'no-cache'
    }

def searchtag(tags):
    tagstring=""
    for i in range(0,len(tags)-1):
        if(i==0):
            tagstring+='{"term":{"tags":%s}}'%{i}
        else:
            tagstring+=',{"term":{"tags":%s}}'%{i}

    postjson='{"sort":["_score",{"created_at_unix":{"order":"desc"}}],' \
             '"query":' \
             '{"bool":{"should":[' \
             '{"constant_score":{"filter":{"match_all":{}},"boost":0}}],' \
             '"minimum_should_match":1,"filter":' \
             '{"bool":{"must":[{"bool":{"must":[%s]}}],' \
             '"must_not":null,"should":[],"minimum_should_match":0}}}}}'%(tagstring)
    headers= {
        "Host": "thorin-us-east-1.searchly.com",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
"Accept": "*/*",
"Accept-Language": "zh-CN",
"Accept-Encoding": "gzip;deflate;br",
"Referer": "https://hanime.tv/search",
"Authorization": "Basic cHVibGljOmlscXd3a2s3Znpxb3Bzand3MXVkcm1yZHQwdDlnb2Mz",
"content-type": "application/json",
"Content-Length": "271",
"Origin": "https://hanime.tv",
"Connection": "keep-alive",
"Pragma": "no-cache",
"Cache-Control": "no-cache}"}
    url='https://thorin-us-east-1.searchly.com/hentai_videos/hentai_video/_search?from=0&size=48'
    r=requests.post(url,data=json.dumps(postjson),headers=headers)
    print(r.text)


def getradom():
    r=requests.get(base_url+radomapi,headers=headers)
    p=json.loads(r.text)
    videos = p['hentai_videos']
    allitemlist = []
    textlist = []
    for key in videos:
        allitemlist.append(key['slug'])
    for i in allitemlist:
        textlist.append(getvideopage(i))
    savetofile(textlist, "radom","radom")
def getvideopage(slug):
    r=requests.get(base_url+detailapi+"%s"%(slug),headers=headers)
    p = json.loads(r.text)
    video=p['transcodes']
    finurl=""
    for a in video:
        if(int(a['height'])==360):
            print(a)
            finurl=a['url']
    return finurl


def getdata(time,page):
    r = requests.get(base_url+pageapi+"time=%s&page=%s"%(time,page),headers=headers)
    r.encoding='utf-8'
    p = json.loads(r.text)
    videos=p['hentai_videos']
    allitemlist=[]
    textlist=[]

    for key in videos:
        allitemlist.append(key['slug'])
    for i in allitemlist:
        textlist.append(getvideopage(i))
    savetofile(textlist,"browser",str(page))
    if (page == 0):
        pagenum = p['number_of_pages']
        for i in range(1, pagenum):
            getdata("month", i)


def savetofile(textlist,path,filename):
    # path="/"+path
    # folder=os.path.exists(path)
    # if not folder:
    #     os.makedirs(path)
    f=open("%s.txt"%(filename),"w")
    for i in textlist:
        f.write(i+"\n")
    f.close()

def gettag(tag,page):
    r = requests.get(base_url+tagapi+"%s?page=%s"%(tag,page),headers=headers)
    p = json.loads(r.text)
    videos = p['hentai_videos']
    allitemlist = []
    textlist = []
    for key in videos:
        allitemlist.append(key['slug'])
    for i in allitemlist:
        textlist.append(getvideopage(i))
    savetofile(textlist,tag,tag+str(page))
    if (page == 0):
        pagenum = p['number_of_pages']
        for i in range(1, pagenum):
            gettag(tag, i)
    print(r.text)
# getdata("month",0)
# tags=[]
# tags.append("3d")
# searchtag(tags)
gettag("3d",0)