# coding:utf-8
'''
@File   :   GH_Crawler.py
@Time   :   2021/10/1
@Author :   Jarcis-cy
@Link   :   https://github.com/Jarcis-cy/Google-Hacking-Crawler
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import argparse
import pprint
import time
import pandas as pd
from urllib import parse

# 获取页面中出现的链接
def getUrl():
	urlList = []
	a = browser.find_elements_by_xpath('//*[@class="g"]/div/div/div/a')
	for i in a:
		tmpUrl = i.get_attribute('href')
		urlList.append(tmpUrl)
	return urlList

# 判断传入的元素是否存在
def isElementExist(by,element):
    flag=True
    try:
        browser.find_element(by,element)
        return flag
    
    except:
        flag=False
        return flag

# 接受爬取页数，开始爬取
def allPage(page,timeSleep):
	allUrl = []
	print("开始爬取")
	for i in range(page):
		time.sleep(timeSleep)
		print("当前为第"+str(i+1)+"页")
		if isElementExist(By.ID,"search"):
			allUrl.append(getUrl())
			print("第"+str(i+1)+"页爬取完成")
			if isElementExist(By.ID,"pnnext"):
				browser.find_element_by_id("pnnext").click()
				if i == page - 1:
					print("全部爬取完成！")
					return allUrl
			else:
				print("没有下一页，全部爬取完成！")
				return allUrl
		else:
			print("不存在元素，全部爬取完成！")
			return allUrl

# 处理url并生成csv
def createCsv(aList,csvName):
	domain = []
	urlL = []
	for i in range(len(aList)):
		for j in range(len(aList[i])):
			parsed_tuple = parse.urlparse(aList[i][j])
			domain.append(parsed_tuple.netloc)
			urlL.append(aList[i][j])
	urlDict = {"domain":domain, "url":urlL}
	df = pd.DataFrame(urlDict)
	df.to_csv(csvName,index=False)

# 传入参数设置
csvName = str(int(time.time())) + ".csv"
parser = argparse.ArgumentParser()
parser.add_argument('--gpu', action="store_false", help='输入该参数将显示chrome，显示爬取过程，默认为False')
parser.add_argument('-s', type=str, default='site:.com', help='请输入你想搜索的google hacking语句，默认为site:.com，以此作为测试')
parser.add_argument('-p', type=int, default=1, help='请输入你想搜索的页数，默认1页')
parser.add_argument('-t', type=int, default=3, help='请输入翻下一页停顿的时间，默认3秒')
parser.add_argument('-r', type=str, default=csvName, help='请输入你想输出的文件名称，默认为'+csvName)
args = parser.parse_args()

# 初始化设置
chrome_options = Options()
if args.gpu:
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get("https://www.google.com")

# 设置爬取目标并开始搜索
browser.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input").send_keys(args.s)
browser.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]").click()

# url处理
createCsv(allPage(args.p,args.t),args.r)

# 结束
browser.quit()
