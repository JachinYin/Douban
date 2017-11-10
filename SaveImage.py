# -*- coding: utf-8 -*-
'''
download bookinfo from www.douban.com
save bookinfo to file 'book.txt'
Author: Jachin
Data: 2017- 11- 09
'''

#标签分类
SortTag = ['小说','名著','历史','哲学','散文','诗歌','互联网','编程']

SortUrl =[]
#获取不同分类下的第一个页面，返回到SortUrl列表中
for item in SortTag:
    SortUrl.append('http://book.douban.com/tag/' + item)

#print SortUrl

from bs4 import BeautifulSoup
import urllib,urllib2
import requests

def getHref(url):
    '''
    获取分类第一页所有书籍的详情页面的链接
    :param html: 分类的链接
    :return: 书籍的详情页面
    '''
    href = []
    heards = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'}
    request = urllib2.Request(url,headers= heards)
    #print request
    try:
        html = urllib2.urlopen(request).read()
        soup = BeautifulSoup(html, 'html.parser')


        for i in range(len(soup.select('h2'))):
            h2 = soup.select('h2')[i]
            for j in range(len(h2.select('a'))):
                href.append(h2.select('a')[j].get('href'))
    except:
        print 'err'
    return href

Href = []
for i in SortUrl:
    Href.append(getHref(i))
    #print(i)  #href保存某个分类下第一页的书籍连接

#print Href
##################################
#书籍页面信息获取
##################################
d = {}
def pa(html):
    '''
    爬取书籍的名字，作者，定价，ISBN，出版社，简介到字典d中
    :param html: 书籍详情链接
    :return: 字典d
    '''
    global  d
    res = requests.get(html)
    s = BeautifulSoup(res.text,'html.parser')
    imageurl = s.find_all('div',id = 'mainpic')[0].a.get('href')


    info = s.find_all('div',id='info')

    info = str(info[0].text.encode('utf-8')).replace(' ','')
    s1 = info.split('\n')

    for i in s1:
        try:
            (key,val) = i.split(':')
            d[key] = val
        except:
            pass

    for i in d.keys():
        if i not in ['ISBN']:
            del d[i]
    d['imageurl'] = 'http:' + imageurl.split(':')[1]
    return d

def SaveImage():
    '''
    下载书籍封面图片
    '''
    try:
        urllib.urlretrieve(d['imageurl'],filename='E:\cover\%s.jpg'%d['ISBN'])
    except:
        pass

#pa('https://book.douban.com/subject/26698660/')
#SaveImage()


#开始爬取
print '开始下载'
c1 = 0
f = open('book.txt','a')
for i in Href:
    print '%s类书籍：'%SortTag[c1]
    c1 += 1
    c2 = 0
    for j in i:
        try:
            pa(j)
            SaveImage()
            print '\t下载第 %d 本书封面'%c2
            c2 += 1
        except:
            print '出错惹'

print '下载完成'
