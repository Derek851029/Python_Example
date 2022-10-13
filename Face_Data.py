import requests
from requests.auth import HTTPDigestAuth
import json
import time
import pyodbc
from datetime import datetime
import os
import threading

def Select_SQL(sql):
    conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=210.68.227.123,3134; DATABASE=Koangyow; UID=sa; PWD=Acme-70472615')
    cursor = conn.cursor()
    sqlstr = sql
    cursor.execute(sqlstr)
    items = []
    for i in cursor:
        d = []
        for x in i:
            d.append(x)
        items.append(d)
    conn.close()
    return items

def Insert_SQL(sql):
    conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=210.68.227.123,3134; DATABASE=Koangyow; UID=sa; PWD=Acme-70472615')
    cursor = conn.cursor()
    sqlstr = sql
    cursor.execute(sqlstr)
    conn.commit()
    conn.close()
    return "success"

def Face_log_Fail():
    date = time.strftime("%Y-%m-%d", time.localtime())
    date_time = time.strftime("%H:%M:%S", time.localtime())
    
    data_time = date + 'T' + date_time + '+08:00'

    while True:
        try:
            time.sleep(0.5)
            data = {
                'AcsEventCond':{
                    'searchID':'1',
                    'searchResultPosition':0,
                    'maxResults':10,
                    'major':5,
                    'minor':76,
                    'startTime':data_time,
                    'timeReverseOrder':True
                }
                }
            r = requests.post('http://192.168.2.21/ISAPI/AccessControl/AcsEvent?format=json',auth=HTTPDigestAuth('admin', 'k1111111'),data=json.dumps(data))
            res_data = json.loads(r.text)

            AcsEvent = res_data['AcsEvent']
            responseStatusStrg = AcsEvent['responseStatusStrg']
            if responseStatusStrg == 'OK':
                InfoList = AcsEvent['InfoList']
                for i in InfoList:
                    recog_time = i['time'][0:19] #日期
                    name = i['name'] #姓名
                    serialNo = i['serialNo'] #Log編號
                    pictureURL = i['pictureURL'] #照片URL
                    employeeNoString = i['employeeNoString'] #工號
                    week = datetime.today().isoweekday()
                    
                    if name == '':
                        name = '未知身分'
                    sql = "select Log_num from [dbo].[FaceRecognition_Log] where Log_num = '"+str(serialNo)+"'"
                    Log_data = Select_SQL(sql)
                    if len(Log_data) == 0:
                        
                        
                        str_date = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
                        r = requests.get(pictureURL,auth=HTTPDigestAuth('admin', 'k1111111'))
                        with open(r'C:/Derek/Koangyow/img/Recong/'+name+'_'+str_date+'.jpeg','wb') as f:
                            f.write(r.content)
                        Image_url = 'http://210.68.227.123:7017/img/Recong/'+name+'_'+str_date+'.jpeg'
                        sql = "insert into [dbo].[FaceRecognition_Log] (Log_num,Name,Number,Create_Date,Week,Image_url) values('{}','{}','{}','{}','{}','{}')".format(str(serialNo),name,employeeNoString,recog_time,week,Image_url)
                        Insert_SQL(sql)
        except Exception as e:
            print(e)
            pass

def Face_log():
    date = time.strftime("%Y-%m-%d", time.localtime())
    date_time = time.strftime("%H:%M:%S", time.localtime())
    
    data_time = date + 'T' + date_time + '+08:00'

    while True:
        try:
            time.sleep(0.5)
            data = {
                'AcsEventCond':{
                    'searchID':'1',
                    'searchResultPosition':0,
                    'maxResults':10,
                    'major':5,
                    'minor':75,
                    'startTime':data_time,
                    'timeReverseOrder':True
                }
                }
            r = requests.post('http://192.168.2.21/ISAPI/AccessControl/AcsEvent?format=json',auth=HTTPDigestAuth('admin', 'k1111111'),data=json.dumps(data))
            res_data = json.loads(r.text)

            AcsEvent = res_data['AcsEvent']
            responseStatusStrg = AcsEvent['responseStatusStrg']
            if responseStatusStrg == 'OK':
                InfoList = AcsEvent['InfoList']
                for i in InfoList:
                    recog_time = i['time'][0:19] #日期
                    name = i['name'] #姓名
                    serialNo = i['serialNo'] #Log編號
                    pictureURL = i['pictureURL'] #照片URL
                    employeeNoString = i['employeeNoString'] #工號
                    week = datetime.today().isoweekday()
                    sql = "select Log_num from [dbo].[FaceRecognition_Log] where Log_num = '"+str(serialNo)+"'"
                    Log_data = Select_SQL(sql)
                    
                    if len(Log_data) == 0:
                        str_date = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
                        r = requests.get(pictureURL,auth=HTTPDigestAuth('admin', 'k1111111'))
                        with open(r'C:/Derek/Koangyow/img/Recong/'+name+'_'+str_date+'.jpeg','wb') as f:
                            f.write(r.content)
                        Image_url = 'http://210.68.227.123:7017/img/Recong/'+name+'_'+str_date+'.jpeg'
                        sql = "insert into [dbo].[FaceRecognition_Log] (Log_num,Name,Number,Create_Date,Week,Image_url) values('{}','{}','{}','{}','{}','{}')".format(str(serialNo),name,employeeNoString,recog_time,week,Image_url)
                        Insert_SQL(sql)
        except Exception as e:
            print(e)
            pass
    
    

if __name__ == "__main__": 
    threading.Thread(target=Face_log).start()
    threading.Thread(target=Face_log_Fail).start()
