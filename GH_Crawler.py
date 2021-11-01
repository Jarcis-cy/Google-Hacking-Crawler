# coding:utf-8
'''
@File   :   GH_Crawler.py
@Time   :   2021/10/1
@Author :   Jarcis-cy
@Link   :   https://github.com/Jarcis-cy
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import time

# 搜索
def getUrl():
	urlList = []
	a = browser.find_elements_by_xpath('//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div/div/div[2]/table/tbody/tr/td/a')
	for i in a:
		tmpUrl = i.get_attribute('textContent')
		urlList.append(tmpUrl)
	return urlList

# 传入参数设置
txtName = str(int(time.time())) + ".txt"
parser = argparse.ArgumentParser()
parser.add_argument('--gpu', action="store_false", help='输入该参数将显示chrome，显示爬取过程，默认为False')
parser.add_argument('-s', type=str, help='请输入你想查询的域名')
parser.add_argument('--tp', type=int, default=4000, help='设置最大爬取数量，默认4000，不建议修改')
parser.add_argument('--wp', type=int, default=0, help='设置想要爬取的数量，请输入100的整数，默认全部爬取（不超过最大爬取数量）')
parser.add_argument('-r', type=str, default=txtName, help='请输入你想输出的文件名称，默认为'+txtName)
args = parser.parse_args()

# 初始化设置
chrome_options = Options()
if args.gpu:
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
chrome_options.add_experimental_option('excludeSwitches',['enable-automation'])
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get("https://securitytrails.com/")

# 登录
email = ""
passwd = ""
browser.find_element_by_xpath('//*[@id="login"]').click()
browser.find_element_by_xpath('//*[@id="email"]').send_keys(email)
browser.find_element_by_xpath('//*[@id="password"]').send_keys(passwd)
browser.find_element_by_xpath('//*[@id="__next"]/div[1]/div[3]/main/div/div/form/div[4]/button').click()
time.sleep(1) # 保险起见
WebDriverWait(browser,300).until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/section/nav/div/div[2]/div/ul/form/div/input')))
print("登陆成功")

browser.find_element_by_xpath('//*[@id="root"]/div/section/nav/div/div[2]/div/ul/form/div/input').send_keys(args.s)
browser.find_element_by_xpath('//*[@id="root"]/div/section/nav/div/div[2]/div/ul/form/div/button').click()
time.sleep(2)
subdomain_num = browser.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/main/div[1]/ul/li[4]/a/span/span[1]').get_attribute('textContent')
subdomain_num = int(subdomain_num.replace(',', ''))
print("共有"+str(subdomain_num)+"条子域名")
browser.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/main/div[1]/ul/li[4]/a').click()
time.sleep(2)
if args.wp == 0:
	if subdomain_num > args.tp:
		nextPageNum = args.tp / 100
	else:
		nextPageNum = int(subdomain_num / 100)
else:
	nextPageNum = args.wp
urlList = []
print("爬取第1页")
WebDriverWait(browser,300).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div/div/div[2]/table/tbody/tr[1]')))
urlList.append(getUrl())
if nextPageNum != 0:
	for i in range(nextPageNum):
		browser.find_element_by_xpath('//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div/div/div[1]/ul/li[8]/a[1]').click()
		print("爬取第"+str(i+2)+"页")
		WebDriverWait(browser,300).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__next"]/div[1]/div[2]/main/div[2]/div[2]/div/div/div[2]/table/tbody/tr[1]')))
		urlList.append(getUrl())
	print("爬取完成")
else:
	print("爬取完成")
browser.quit()
f = open(args.r,"w")
for i in urlList:
	for j in i:
		f.write(j + "\n")
f.close()
print("文件已生成")
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
