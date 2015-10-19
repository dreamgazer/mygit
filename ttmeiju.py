#-*- coding: utf8 -*-
import urllib
import urllib2
import re
import sys
import webbrowser
from Tkinter import *
from tkSimpleDialog import *

sys.path.append("libs")

baseurl='http://www.ttmeiju.com/meiju/'
name='The.Big.Bang.Theory'
pagenum=1
Length=0


class getweb:
    def __init__(self,name,pagenum):
        self.name=name
        self.pagenum=pagenum

    def getcontent(self):
        url=baseurl+self.name+'.html?page='+str(self.pagenum)
        request=urllib2.Request(url)
        page=urllib2.urlopen(request)
        return page

    def getmenu(self):
      page=self.getcontent()
      content=page.read()
      menu = re.compile('<tr class="Scontent">.*?<td>(.*?)</td>.*?html">(.*?)</a>.*?<a href=.*? rel.*?title=.*?><img.*?<a href=.*? rel.*?title=.*?><img.*?<td>(.*?)</td>.*?<td>(.*?)</td>',re.S)
      menus = re.findall(menu,content)
      menulist=[]
      for m in menus:
           me= m[1]+' '+m[2]+' '+m[3]
           menulist.append(me)
      return menulist
    
    def gettorrent(self):
      page=self.getcontent()
      content=page.read()
      torrentcontent = re.compile('<tr class="Scontent">.*?<td>.*?</td>.*?html">.*?</a>.*?<!--/if}-->(.*?)<td>.*?</td>.*?<td>.*?</td>',re.S)
      torrentcontents = re.findall(torrentcontent,content)
      return torrentcontents


        
class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("ttmeiju")
        menubar=Menu(self.window)
        self.window.config(menu=menubar)
        tkmenu=Menu(menubar,tearoff=0)
        menubar.add_cascade(label=("菜单").decode('utf8'),menu=tkmenu)
        tkmenu.add_command(label=("剧目搜索").decode('utf8'),command=self.search)                
        tkmenu.choices = Menu(tkmenu)
        tkmenu.choices.add_command(label=("每日秀").decode('utf8'),command=lambda:self.choose('The.daily.show'))
        tkmenu.choices.add_command(label=("生活大爆炸").decode('utf8'),command=lambda:self.choose('The.Big.Bang.Theory'))
        tkmenu.choices.add_command(label=("维京传奇").decode('utf8'),command=lambda:self.choose('Vikings'))
        tkmenu.add_cascade(label=("剧目选择").decode('utf8'),menu=tkmenu.choices)
        tkmenu.add_command(label=("选择页码").decode('utf8'),command=self.pagechoose)
        self.showcontent(name,pagenum)
        self.window.mainloop()

    def showcontent(self,name,pagenum):
        i=0
        n=1
        global Length
        self.address=[]
        mj=getweb(name,pagenum)
        self.m_list=mj.getmenu()        
        t_list=mj.gettorrent()
        torrent = re.compile('<a href=\'(.*?)\' rel=.*?title=\'(.*?)\'',re.S)
        for tc in t_list:
            torrents = re.findall(torrent,tc)            
            self.address.append(torrents)                
        Button(self.window,text=('上一页').decode('utf8'),bg="grey",command=lambda: self.formerpage()).grid(row=1,column=2,sticky=E)        
        Button(self.window,text=('下一页').decode('utf8'),bg="grey",command=lambda: self.nextpage()).grid(row=1,column=3)
        Label(self.window,compound = 'left',height = 1,width =37,text= name+'                  '+('第').decode('utf8')+' '+str(pagenum)+' '+('页').decode('utf8')).grid(row=1,column=1,sticky=W)
        while i<Length:
          if n==1:
               Label(self.window,height = 2,width = 70,text= ' ',bg="white").grid(row=i+2,column=1,columnspan=3,sticky=W+E)                   
          else:
              Label(self.window,height = 2,width = 70,text= ' ').grid(row=i+2,column=1,columnspan=3,sticky=W+E)
          i=i+1    
        i=0      
        while i<len(self.m_list):
          self.m_list[i] = self.m_list[i].decode("gbk")
          if n==1:
               Label(self.window,height = 2,width = 70,text= self.m_list[i],bg="white").grid(row=i+2,column=1,columnspan=2)
          else:
              Label(self.window,height = 2,width =70,text= self.m_list[i]).grid(row=i+2,column=1,columnspan=2)
          self.cd(i)
          i=i+1
          n=0-n
          
          Length=len(self.m_list)
          
    def nextpage(self):
        global pagenum
        pagenum=pagenum+1
        self.showcontent(name,pagenum)
        
    def formerpage(self):        
       global pagenum        
       if pagenum>1:
        pagenum=pagenum-1
        self.showcontent(name,pagenum)

    def choose(self,showname):    
         global name
         name=showname
         self.showcontent(name,1)
         
    def showresult(self,keyword):
        s=keyword
        sc=urllib.quote(s.encode('gb2312'))
        surl='http://www.ttmeiju.com/search.php?keyword='+str(sc)+'&range=0'
        request=urllib2.Request(surl)
        spage=urllib2.urlopen(request)
        scontent=spage.read()
        gettitle = re.compile('<td align="left">.*?<a href=".*?/meiju/(.*?).html" target="_blank">.*?</a></td>',re.S)
        search = re.compile('<td align="left">.*?<a href=.*?target="_blank">(.*?)</a></td>',re.S)
        results = re.findall(search,scontent)
        self.titles= re.findall(gettitle,scontent)
        self.resultwindow = Tk()
        self.resultwindow.title("result")
        i=0
        if len(results)==0:
            Label(self.resultwindow,text="no result").grid(row=2,column=2)            
        while i<len(results):
          results[i] = results[i].decode("gbk")
          Label(self.resultwindow,text= results[i]).grid(row=i+2,column=1)
          number=[]
          number.append(i)
          self.searchbutton(i)
          i=i+1
        self.resultwindow.mainloop()
        
    def searchbutton(self,number):    
        Button(self.resultwindow,text=("选择").decode('utf8'),command=lambda: self.add(self.titles,number)).grid(row=number+2,column=5)
        
    def search(self):
         keyword=askstring(title = ('搜索').decode('utf8'),prompt = ('输入关键字：').decode('utf8'))    
         if keyword:             
           self.showresult(keyword)

    def showtorrents(self,number):
        self.torrentwindow = Tk()
        self.torrentwindow.title("result")
        i=0
        while i<len(self.address[number]):
          self.torrentsbutton(number,i)                    
          i=i+1
        self.torrentwindow.mainloop()
        
    def torrentsbutton(self,number,i):
        torrenturl=self.address[number][i][0]
        Label(self.torrentwindow,text=self.m_list[number]).grid(row=1,column=1)
        Button(self.torrentwindow,text=self.address[number][i][1].decode('gbk'),command=lambda: webbrowser.open(torrenturl)).grid(row=i+2,column=1)

    def add(self,titles,number):
        global name
        global pagenum
        pagenum=1
        name=titles[number]
        self.showcontent(name,pagenum)
        
    def cd(self,n):
        Button(self.window,text=('下载').decode('utf8'),height = 1,width = 5,command=lambda: self.showtorrents(n)).grid(row=n+2,column=3)

    def pagechoose(self):        
         num=askstring(title = ('选择页码').decode('utf8'),prompt = ('输入页码：').decode('utf8'))
         if num:
             int(num)
             self.showcontent(name,num)
        

GUI()
    




