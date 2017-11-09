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
    SortUrl.append('https://book.douban.com/tag/' + item)

#print SortUrl

from bs4 import BeautifulSoup
import urllib
import requests

def getHref(url):
    '''
    获取分类第一页所有书籍的详情页面的链接
    :param html: 分类的链接
    :return: 书籍的详情页面
    '''
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    h2 = []
    href = []
    for i in range(len(soup.select('h2'))):
        h2 = soup.select('h2')[i]
        for j in range(len(h2.select('a'))):
            href.append(h2.select('a')[j].get('href'))
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
    info = s.find_all('div',id='info')
    name = s.find_all('h1')[0].span.text.encode('utf-8')
    author = ''.join(s.find_all('div',id='info')[0].a.text.encode('utf-8').split('\n')).replace(' ', '')
    intro = s.find_all('div',class_='intro')[0].text.encode('utf-8').replace(' ', '\n')

    info = str(info[0].text.encode('utf-8')).replace(' ','')
    s1 = info.split('\n')

    for i in s1:
        try:
            (key,val) = i.split(':')
            d[key] = val
        except:
            pass

    for i in d.keys():
        if i not in ['ISBN','出版社','定价']:
            del d[i]
    d['简介'] = intro
    d['作者'] = author
    d['书名'] = name

    return d

#开始爬取
c1 = 0
f = open('book.txt','a')
for i in Href:
    print '爬%s类书籍：'%SortTag[c1]
    c1 += 1
    c2 = 0
    for j in i:
        try:
            pa(j)
            if '展开全部' in d['简介']:#发现简介有’展开全部‘字样的跳过，因为这部分处理涉及JS
                print '跳过'
            else:
                print '\t爬第 %d 本书'%c2
                c2 += 1
                for i in d.keys():
                    s1 = i + ' ' + d[i] + '\n'
                    f.write(s1)
        except:
            print '出错惹'

f.close()
print '爬取完成'

