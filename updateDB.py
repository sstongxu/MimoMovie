#-*- codeing = utf-8 -*-
#@Time :  
#@Author: Mianbao
#@File : updateDB.py
#@Software : PyCharm

from multiprocessing import Pool, Lock

import requests
from bs4 import BeautifulSoup
import random
import re
from DBManger import sqlite_db
import time


def get_headers( url, use='pc'):
    '''获取标准的headers'''
    pc_agent = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0"
    ]
    phone_agent = [
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        "UCWEB7.0.2.37/28/999",
        # "NOKIA5700/ UCWEB7.0.2.37/28/999",
        "Openwave/ UCWEB7.0.2.37/28/999",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"
    ]
    """user_agent部分来源:https://blog.csdn.net/IT__LS/java/article/details/78880903"""
    referer = lambda url: re.search(
        "^((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)", url).group()
    """正则来源:https://www.cnblogs.com/blacksonny/p/6055357.html"""
    if use == 'phone':  # 随机选择一个
        agent = random.choice(phone_agent)
    else:
        agent = random.choice(pc_agent)
    headers = {
        'User-Agent': agent,
        'Referer': referer(url),
        'DNT': "1",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    return headers

def searchTotalMovieNumber():
    '''获取网页总页数'''
    host = "http://www.xxi5.cn/mv/"
    resp = requests.post(host, headers)
    selector = BeautifulSoup(resp.text, 'html.parser')
    for video_url in selector.find_all('a'):
        if video_url.get('class') != None and "end" in video_url.get('class')[0]:
            return video_url.string.replace("...", "")

def init(l,l2):
    global lock
    global lock2
    lock = l
    lock2 = l2
def getMovieEveryPage():
    '''扫描每一页'''
    TotalNum = searchTotalMovieNumber()
    totalPages = []
    for i in range(0,int(TotalNum)):
        host = r"http://www.xxi5.cn/mv/1-0-0-0-0-"+str(i)+".html"
        totalPages.append(host)


    lock = Lock()
    lock2 = Lock()
    pool = Pool(8, initializer=init, initargs=(lock,lock2))  # 创建进程池
    pool.map(getMovieData, totalPages)
    print("整理每页url完成")

def getMovieData(host):
    '''扫描电影名称和链接'''
    resp = requests.post(host, headers=headers)
    selector = BeautifulSoup(resp.text, 'html.parser')
    videoNum = 0
    for videoT_url in selector.find_all('a'):
        if videoT_url.get('class') != None and "thumbnail" in videoT_url.get('class'):
            videoNum +=1
            moviename = videoT_url.get("title")
            movieresource = "http://www.xxi5.cn" + videoT_url.get("href")
            moviepicture = videoT_url.img.get("data-original")
            # print(moviename)
            # print(movieresource)
            # print(moviepicture)
            try:
                movieid = sq.addMovieInformation(moviename, movieresource, moviepicture)
                get_DownLoad_page(movieresource, movieid)

            except Exception as e:
                print("getMovieDataError:"+str(e))
                continue

            # print("==========================")
            time.sleep(1)
    # print(videoNum)

def get_DownLoad_page(host, movieid):
    '''扫描下载页面和详细信息'''
    resp = requests.post(host, headers)
    selector = BeautifulSoup(resp.text, 'html.parser')
    DownloadNum = 0
    for video_url in selector.find_all('tr'):
        if video_url.get('class') != None and "even" in video_url.get('class') or "odd" in video_url.get('class'):
            secondSelector = BeautifulSoup(str(video_url),"lxml")
            tdConter = secondSelector.find_all("td")

            resourcename = video_url.a.text
            resourcequality = tdConter[0].text
            resourcefoundpage = "http://www.xxi5.cn" + video_url.a.get("href")
            resourcesize = tdConter[2].text
            resourcedate = tdConter[3].text
            downloadnum = tdConter[4].text
            resourcedownload = findMagnet(resourcefoundpage)
            # print("名称：" + resourcename)
            # print("画质："+ resourcequality)
            # print(resourcefoundpage)
            # print("大小：" + resourcesize)
            # print("时间：" + resourcedate)
            # print("下载数：" + downloadnum)
            # print("=========================")
            DownloadNum += 1
            for url in resourcedownload:
                try:
                    # lock2.acquire()
                    sq.addResourceInformation(resourcename,resourcequality,resourcefoundpage,resourcesize,resourcedate,downloadnum,url,movieid)
                    # lock2.release()
                except Exception as e:
                    print("get_DownLoad_pageError："+str(e))
                    continue
        time.sleep(1)

def findMagnet(host):
    '''获取种子链接'''
    resp = requests.post(host, headers)
    selector = BeautifulSoup(resp.text, 'html.parser')
    Downloadurl = []
    for video_url in selector.find_all('a'):
        if video_url.get('class') != None and "btn-primary" in video_url.get('class'):
            Downloadurl.append(video_url.get("href"))
    return Downloadurl
# headers = get_headers("http://www.xxi5.cn/mv/")
headers = get_headers("http://www.xxi5.cn/tv/")
sq = sqlite_db()
if __name__ == '__main__':


    getMovieEveryPage()