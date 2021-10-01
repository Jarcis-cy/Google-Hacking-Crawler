# Google-Hacking-Crawler
----
该脚本可输入Google Hacking语句，自动调用Chrome浏览器爬取结果

### 环境配置
1. `python -m pip install -r requirements.txt`
2. 下载Chrome浏览器，然后去`https://npm.taobao.org/mirrors/chromedriver/`下载对应之前下载的Chrome浏览器版本的chromedriver.exe
3. 将下载好的chromedriver.exe放入python.exe的所在文件夹，然后再放入chrome.exe的所在文件夹。
4. 将chrome.exe的所在文件夹设到系统变量中。
### Help
```
optional arguments:
  -h, --help  show this help message and exit
  --gpu       输入该参数将显示chrome，显示爬取过程，默认为False
  -s S        请输入你想搜索的google hacking语句，默认为site:.com，以此作为测试
  -p P        请输入你想搜索的页数，默认1页
  -t T        请输入翻下一页停顿的时间，默认3秒
  -r R        请输入你想输出的文件名称，默认为1633096774.csv
```
### 例子
`python GH_Crawler.py -s "site:.com and inurl:.php?id=" -p 2 -t 5`
