# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 09:09:00 2020

@author: Qing

google新聞的爬蟲
"""

import requests
from bs4 import BeautifulSoup
import pyodbc
import pandas as pd
import datetime, time, threading
from queue import Queue


def search(keyword):
    '''從google爬取新聞'''
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0'
    #user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    headers = {'user-agent':user_agent}
    
    datalist = []
    page = 0
    url = 'https://www.google.com/search?q={}&tbm=nws&tbs=sbd:1'
    
    while True:
        start = '&start=' + str(page*10)
        
        r = requests.get(url.format(keyword)+start, headers=headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        
        news = soup.find('div', id='rso')
        
        if news == None:
            return "None Data"
        datas = news.find_all('g-card')
        
        for i in datas:
            newsTime = i.find('span',class_='WG9SHc').text
            #print(newsTime)
            if '天' in newsTime:
                print('done')
                return datalist
            
            
            title = i.find('div',class_='JheGif').text
            source = i.find('div',class_='XTjFC WF4CUc').text
            newsUrl = i.find('a')['href']
            
            data = [title.replace("'", "''"), newsUrl, source.replace("'", "''"), newsTime]
            datalist.append(data)
        break  
        page += 1
        print(' ... d(`･∀･)b ')
        time.sleep(1)
    return datalist
    
    
def getdate(url, source, ptime, q, t):
    
    gdate = ''
    try:
        r = requests.get(url, timeout = 5)
        soup = BeautifulSoup(r.text, 'lxml')
        pdate = datetime.datetime.strptime(soup.find('time')['datetime'], "%Y-%m-%dT%H:%M:%S%z")
        gdate = pdate.strftime('%Y-%m-%d %H:%M:%S')
    except:
        pass
    
    if len(gdate) == 0:
        if '時' in ptime or 'hour' in ptime:
            ghours = int(ptime.split(' ')[0])
            gdate = datetime.datetime.now()+datetime.timedelta(hours= -ghours)
            gdate = gdate.strftime("%Y-%m-%d %H:%M:%S")
        elif '分' in ptime or 'minute' in ptime:
            gminutes = int(ptime.split(' ')[0])
            gdate = datetime.datetime.now()+datetime.timedelta(minutes= -gminutes)
            gdate = gdate.strftime("%Y-%m-%d %H:%M:%S")
    
    print(' ... ( •ω•)✧ ...')
    q.put([t,gdate])


def wtosql(keyword, linkdata, Owner):
    print('get the news public time')
    print('please wait a minute')
    q = Queue()
    threads = []
        
    for t,i in enumerate(linkdata):
        th_a = threading.Thread(target=getdate, args=(i[1],i[2],i[3],q,t,))
        th_a.start()
        threads.append(th_a)
        
        if len(threads)%10 == 0:
            for i in threads:
                i.join()
            threads = []
            time.sleep(0.2)
    
    for i in threads:
        i.join()
    
    for i in range(len(linkdata)):
        datedata = q.get()
        linkdata[datedata[0]][-1] = datedata[1]
        
    print('done')
    print('start to save datas in sql')
    
    conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=DESKTOP-4H6RDTK\MSSQLSERVER2012; DATABASE=Customer; UID=sa; PWD=Acme-70472615') 

    cursor = conn.cursor()
    
    cursor.execute('select SYSID,href from [dbo].[AutoSendSearch]')
        
    datas = []
    for i in cursor:
        data = []
        for j in i:
            data.append(j)
        datas.append(data)
    
    datas = pd.DataFrame(datas)
    
    if(len(datas) != 0):
        for i in linkdata:
            write = True
            for j in datas.loc[:,1]:
                if i[1] in j:
                    write = False
                    break
            if write:
                sqlstr = '''Insert into [dbo].[AutoSendSearch]
                (keyword, title , href, source, public_time, Owner)
                values
                ('{}', '{}', '{}', '{}', '{}','{}')
                '''.format(keyword, i[0], i[1], i[2], i[3],Owner)
                #print(sqlstr)
                cursor.execute(sqlstr)
            
            
    else:
        for i in linkdata:
            cursor.execute('''Insert into [dbo].[AutoSendSearch] 
            (keyword, title , href, source, public_time, Owner)
            values
            ('{}', '{}', '{}', '{}', '{}','{}')
            '''.format(keyword, i[0], i[1], i[2], i[3], Owner))

    conn.commit()
    
    conn.close()
    print('done')

def getkeyword(sql):
    '''從資料庫撈取關鍵字'''
    conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=DESKTOP-4H6RDTK\MSSQLSERVER2012; DATABASE=Customer; UID=sa; PWD=Acme-70472615') 

    cursor = conn.cursor()
    
    sqlstr = sql
    
    cursor.execute(sqlstr)
    
    keyword = []
    
    for i in cursor:
        for j in i:
            keyword.append(j)
            
    conn.close()
    return keyword

def findOwner(Owner_sql):
    conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=DESKTOP-4H6RDTK\MSSQLSERVER2012; DATABASE=Customer; UID=sa; PWD=Acme-70472615') 

    cursor = conn.cursor()
    
    sqlstr = Owner_sql
    
    cursor.execute(sqlstr)
    
    Owner = []
    
    for i in cursor:
        for j in i:
            Owner.append(j)
            
    conn.close()
    return Owner
            

def controller():
    try:
        Ownerarray = findOwner("SELECT SYSID FROM [dbo].[DispatchSystem] WHERE Agent_Status = '在職'")
        for Owner in Ownerarray:
            keyword = getkeyword("SELECT BUSINESSNAME FROM [dbo].[BusinessData] WHERE Owner='"+str(Owner)+"' AND Type='保留'")
            for t,i in enumerate(keyword) :
                newsdata = search(i)
                wtosql(i, newsdata, Owner)
            if len(keyword) == 0:
                pass
            else: #if t+1 != len(keyword):
                print('Prepare to find next keyword...')
                time.sleep(5)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    controller()








