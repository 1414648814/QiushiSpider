# coding=utf-8
import urllib
import urllib2
import re
import  thread
import time

class QSBK:
    # 初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        # 初始化headers
        self.headers = {'User-Agent' :self.user_agent}
        # 存放段子的变量，每个元素是每一页的段子们
        self.stories = []
        # 程序是否继续运行
        self.enable = False
    # 传入某一页的索引获得页面代码
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print "error",e.reason
                return None
    # 传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "page load error"
            return None
        # pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</.*?number">(.*?)</',re.S)
        pattern = re.compile(r'<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>.*?<i class="number">(.*?)</i>.*?<i class="number">(.*?)</i>', re.S)
        # 1.用户名字
        # 2.段子内容
        # 3.点赞个数
        # 4.评论个数

        items = re.findall(pattern,pageCode)
        pageStories = []

        for item in items:
            replaceBR = re.compile('<br/>')
            content = re.sub(replaceBR,"\n",item[1])
            pageStories.append([item[0].strip(),content.strip(),item[2].strip()])
        return pageStories
    # 加载并提取页面的内容，加入到列表中
    def loadPage(self):
        # 如果当前未看的页数少于2页，则加载新一页
        if self.enable==True:
            if len(self.stories)<2:
                # 获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                # 将该页的段子存放在全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex +=1
    # 每次敲回车打印输出一个段子
    def getOneStory(self,pageStories,page):
        for story in pageStories:
            # 等待用户输入
            input = raw_input()
            # 判断一下是否要加载新页面
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人：%s\t 赞：%s\n%s" %(page,story[0],story[2],story[1])

    def start(self):
        print u'正在读取糗事百科，回车查看，Q退出'
        self.enable = True
        # 先加载一页内容
        self.loadPage()
        # 控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                # 从全局list中获取一页的段子
                pageStories = self.stories[0]
                nowPage +=1
                # 删除取出的段子
                del self.stories[0]
                # 输出段子
                self.getOneStory(pageStories,nowPage)

if __name__=='__main__':
    spider = QSBK()
    print spider.start()