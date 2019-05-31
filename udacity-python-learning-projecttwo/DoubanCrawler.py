# -*- coding='utf-8' -*-
import requests
import bs4
import expanddouban
import urllib
from lxml import etree
import csv
import re
import pandas as pd
import time

'''

1.这是Udacity python编程入门的项目二：爬取豆瓣电影信息 的完整代码（个人写的，可能与其他人写的有差异）

2.这段代码虽然是爬虫代码，但是尽量不要在以后学习爬虫的过程中完全根据作业要求的思路来写，这种代码足够交作业并且毕业，但是不适合生产，因为运行起来非常笨重。

3.仔细阅读下面的注释，对理解这段代码有很大的帮助

4.自行写代码的时候可以更改一些代码，例如很多函数或者列表的名称我起的比较繁琐，也希望不被检查出来抄袭，多少要改一些内容。

5.上面有一些引用的包，非python自带的请自行到命令栏用pip或者pip3安装，否则运行会报错找不到包（如果不知道有哪些包可以先运行一下，看报错找不到哪些包来知道自己缺少哪些包）

6.我一起给了网页第一页的爬取结果，没有爬取单个类型里面的所有电影信息，若在爬取全网页时出现问题请自行解决（应该是没什么问题）

'''

#任务1
def constant(so,ra):
	Base_Url = "https://movie.douban.com/tag/#/?"
	Sort = "sort="
	Range = "range="
	Tags = "tags="
	baseUrl = Base_Url+Sort+str(so)+'&'+Range+str(ra)+'&'+Tags
	return baseUrl


def getMovieUrl(category='',location=''):
	url = str(constant('U','0,10'))+str(category)+','+str(location)
	return url


#任务2
def getHtmlTxT(url,loadmore = False,waittime = 2):
	#这里loadmore 在True的时候会翻页，False的时候只开第一页，测试代码的时候最好开成False
	#作业提交的时候并不需要你完全爬完一个类型的所有电影，只需要在loadmore = False的情况下上传运行结果就足够了。
	#waittime主要是打开网页多久不反应了就退出，如果网速不好可以提高一点，如果太高在类型全电影信息爬取的时候可能会翻页过多，几个小时可能都到不了底。
	html = expanddouban.getHtml(url,loadmore,waittime) 
	soup = bs4.BeautifulSoup(html, "html.parser")
	return soup


#任务3
class Movie:
	def __init__(self,name,rate,location,category,info_link,cover_link):
		self.name = movie_name
		self.rate = movie_rate
		self.location = movie_location
		self.category = movie_category
		self.info_link = movie_info_link
		self.cover_link = movie_cover_link


MovieList = []
def getMovies(category='', location=''):	
	cate = category
	html = getHtmlTxT(getMovieUrl(cate,''))
	movie_category = []
	movie_name = []
	movie_rate = []
	movie_location = []
	movie_info_link = []
	movie_cover_link = []

	names = html.find_all("span",{"class":"title"})
	for name in names:
		movie_name.append(name.get_text())

	rates = html.find_all("span",{"class":"rate"})
	for rate in rates:
		movie_rate.append(str(rate.get_text()))
	
	#这里由于电影的具体类型和国家只会在单个电影信息页面显示所以需要打开爬取到的每一个链接
	info_links = html.find_all("a",{"class":"item"})
	for info_link in info_links:
		movie_info_link.append(info_link.get('href'))
		header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
		response = requests.get(info_link.get('href'),headers = header)
		html = response.text
		moviepage = bs4.BeautifulSoup(html, "lxml")
		cover = moviepage.find("img",{"title":"点击看更多海报"})
		movie_cover_link.append(cover.get('src'))
		moviepage = str(moviepage)
		movie_location.append(re.search('<span class="pl">制片国家/地区:</span>( .*?)<br/>',moviepage).group(1))
		time.sleep(5) #每打开一次单个电影信息主页后，挂5秒，不然很容易被反爬虫，封ip

	lon = int(len(movie_name))	
	for i in range(0,lon):
		movie_category.append(cate)

	List = list(zip(movie_name,movie_rate,movie_location,movie_category,movie_info_link,movie_info_link))  
	return List


#MovieList是本次爬虫爬到的所有的电影的列表
#下面的类型自己随意选择
ListOne = getMovies('爱情','')
MovieList.extend(ListOne)

ListTwo = getMovies('动作','')
MovieList.extend(ListTwo)

ListThree = getMovies('喜剧','')
MovieList.extend(ListThree)


totalnum = int(len(MovieList))
topmovies = []  #筛选出所有评分大于等于9分的电影
for i in range(0,totalnum-1):
	if float(MovieList[i][1])>= 9.0:
		topmovies.append(MovieList[i])
	else:
		continue

#任务5
name = ['电影名字','电影评分','电影地区','电影类型','电影页面链接','电影海报图片链接']
test = pd.DataFrame(columns=name,data=topmovies)
test.to_csv('d:/movies.csv',encoding='utf-8')  #这里面我暂时把文件都输出在了D盘目录下

def anaysis(List):
	coutries = []  #统计所有出现过的国家
	num = int(len(List))
	for i in range(0,num-1):
		coutries.append(List[i][2])

	countriesnumbers = {}  #所有的国家的数量
	for item in coutries:
		countriesnumbers.update({item:coutries.count(item)})
	allCountiesNumber = zip(countriesnumbers.values(),countriesnumbers.keys())
	allCountiesNumber = sorted(allCountiesNumber,reverse=True)
	topcountries = []  #前三国家
	for i in range(0,4):
		topcountries.append(allCountiesNumber[i])
	#得到比例
	a = str(round(float(int(topcountries[0][0])/int(len(MovieList)))*100,5))+'%'
	b = str(round(float(int(topcountries[1][0])/int(len(MovieList)))*100,5))+'%'
	c = str(round(float(int(topcountries[2][0])/int(len(MovieList)))*100,5))+'%'

	out = str(str(List[0][3])+"电影数量排名前三的地区是："+str(topcountries[0][1])+'、'+str(topcountries[1][1])+'、'+str(topcountries[2][1])+'。'+"排名第一的是："+str(topcountries[0][1])+"，他的占比是："+str(a)+"。排名第二的是"+str(topcountries[1][1])+"，他的占比是："+str(b)+"。排名第三的是"+str(topcountries[2][1])+"，他的占比是："+str(c)+'。')
	return(out)


#任务6
with open('d:/output.txt',mode='w',encoding='utf-8') as f: #这里的文件输出目录也是D盘
	f.write(anaysis(ListOne)+'\n'+ anaysis(ListTwo)+'\n'+ anaysis(ListThree))







