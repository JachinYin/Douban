# Douban

爬取豆瓣书籍信息

包括**ISBN，书名，作者，出版社，定价，简介，类型**

1. ToFile.py

  ​-爬取到的内容保存到book.txt中

2. ToSqlServer

  -爬取到的内容到SqlServer中

  -数据库BookStore

  -表Book



**ps**：网页爬取使用了bs4，urllib，requests库

​	接入数据库使用的是pymssql

​	尝试使用pyodbc却一直连接不上数据库，没找到解决办法，最后选择psmssql就没问题了。