from flask import Flask, current_app, request, Response
from flask_cors import CORS
from requests.auth import HTTPDigestAuth
import json
import requests
import pyodbc
from datetime import datetime
import threading
import time
import pandas as pd

# # 獲取主機名
# hostname = socket.gethostname()
# #獲取IP
# ip = socket.gethostbyname(hostname)

app = Flask(__name__)
CORS(app)

def Line_Post(text,UserID):
    url = 'http://210.68.227.123:7014/PushFaceData.aspx/PushLineMsg'
    # LINE 群發訊息資料 --> text: 要發的訊息內容
    data = {'ID':UserID,'msg':text}
    headers = {
              'Content-Type': 'application/json'
            }
    r = requests.post(url,headers=headers ,data = json.dumps(data,separators=(',', ':')))
    return 'success'

def Select_SQL(sql):
    conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=210.68.227.123,3134; DATABASE=JohanSchook; UID=sa; PWD=Acme-70472615')
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
    conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=210.68.227.123,3134; DATABASE=JohanSchook; UID=sa; PWD=Acme-70472615')
    cursor = conn.cursor()
    sqlstr = sql
    cursor.execute(sqlstr)
    conn.commit()
    conn.close()
    return "success"

def Create_Put_Face_To_Device():
    while True:
        time.sleep(3)
        today = datetime.today().strftime('%Y-%m-%d')
        formate_today = today + 'T00:00:00'
        try:
            sql = "select Name,Serial_Number,Img_url FROM [KarlSchool].[dbo].[Person_List] where Flag = 0"
            data = Select_SQL(sql)
            if len(data) != 0:
                for i in data:
                    req_data = {
                    'UserInfo':{
                        'employeeNo':i[1],
                        'name':i[0],
                        'userType':'normal',
                        'Valid':{
                            'enable':True,
                            'beginTime':formate_today,
                            'endTime':'2037-12-31T23:59:59',
                            'timeType':'local',
                        },
                        "doorRight":"1",
                        "RightPlan":[{
                            "doorNo":1,
                            "planTemplateNo":"1"
                        }],
                    }
                    }
                    #機器建立人員
                    r = requests.put('http://10.1.1.233/ISAPI/AccessControl/UserInfo/SetUp?format=json',auth=HTTPDigestAuth('admin', 'Acme70472615'),data=json.dumps(req_data)) 
                    if r.status_code == 200:
                        req_data = {
                                'faceURL': i[2],
                                'faceLibType':'blackFD',
                                'FDID':'1',
                                'FPID':i[1]
                                }
                        #放置人臉
                        r= requests.put('http://10.1.1.233/ISAPI/Intelligent/FDLib/FDSetUp?format=json',auth=HTTPDigestAuth('admin', 'Acme70472615'),data=json.dumps(req_data))
                        if r.status_code == 200:
                            sql = "update [dbo].[Person_List] set Flag = 1 where Serial_Number = '"+i[1]+"'"
                            Insert_SQL(sql)
                        else:
                            sql = "insert into SystemLog(PageName,PageFunc,PageLog,EX)values('python','Create_Put_Face_To_Device/putFace','海康建立','"+r.text+"')"
                            Insert_SQL(sql)
                    else:
                        sql = "insert into SystemLog(PageName,PageFunc,PageLog,EX)values('python','Create_Put_Face_To_Device/Create_Person','海康建立','"+r.text+"')"
                        Insert_SQL(sql)
            sql = "select Serial_Number FROM [KarlSchool].[dbo].[Person_List] where Status = '刪除'"
            data = Select_SQL(sql)
            if len(data) != 0:
                for i in data:
                    req_data = {
                            'UserInfoDelCond':{
                                    'EmployeeNoList':[{'employeeNo':i[0]}],
                                    'operateType':'byTerminal',
                                    'terminalNoList':[1]
                                }
                            }
                    #機器刪除人員
                    r= requests.put('http://10.1.1.233/ISAPI/AccessControl/UserInfo/Delete?format=json',auth=HTTPDigestAuth('admin', 'Acme70472615'),data=json.dumps(req_data))
                    if r.status_code == 200:
                        sql = "update [dbo].[Person_List] set Flag = 2,Status = '完整刪除' where Serial_Number = '"+i[0]+"'"
                        Insert_SQL(sql)
            #同步人員
            # data = {
            #         'UserInfoSearchCond': {
            #             "searchID":'1',
            #             "searchResultPosition":0,
            #             "maxResults": 10,
            #             },
            #         }
            # r= requests.post('http://10.1.1.233/ISAPI/AccessControl/UserInfo/Search?format=json',auth=HTTPDigestAuth('admin', 'Acme70472615'),data=json.dumps(data))
            # data = json.loads(r.text)['UserInfoSearch']['UserInfo']
            # for i in data:
            #     Serial_Number = i['employeeNo']
            #     sql = "select Serial_Number from [dbo].[Person_List] where Status = ' Add' and Account is null and Serial_Number='"+Serial_Number+"'"
            #     Person = Select_SQL(sql)
            #     if len(Person) == 0:
            #         if Serial_Number != 1 or Serial_Number != 2:
            #             sql = "insert into [dbo].[Person_List](Name,) values()"
                    
        except Exception as e:
            sql = "insert into SystemLog(PageName,PageFunc,PageLog,EX)values('python','Create_Put_Face_To_Device','Create_Put_Face_To_Device','"+str(e)+"')"
            Insert_SQL(sql)
    
def Check_Late_Student():
    Status = ''
    while True:
        time.sleep(30)
        now = datetime.now()
        str_time = now.strftime("%H:%M")        
        week = datetime.today().isoweekday()
        
        date = datetime.now().strftime('%Y-%m-%d')
        if str_time == '08:10':
            if week != 6 or week != 7:
                if Status == '':
                    try:
                        sql = "select a.Class,a.Name,b.Class_Status from [dbo].[Person_List] a left join [dbo].[FaceRecognition_Log] b on a.Serial_Number = b.Number and b.Create_Date = '"+date+"' where b.Class_Status is null and a.Status = ' Add' and a.Account is null"
                        late_student = Select_SQL(sql)
                        if len(late_student) != 0:
                            Class = []
                            Name = []
                            for i in late_student:
                                Class.append(i[0])
                                Name.append(i[1])
                            
                            
                            dic = {
                                "Name": Name, 
                                "Class": Class,
                            }
                            df = pd.DataFrame(dic)
                            
                            Class = set(Class)
                            Class = list(Class)
                            for i in range(len(Class)):
                                fliter = (df['Class'] == Class[i])
                                New_df = df[fliter]
                                All_Name = New_df['Name'].values
                                
                                Name_str = str(list(All_Name))
                                text = Name_str + ' Not in class'
                                
                                sql = "select UserID from [dbo].[Class_List] where Class_Name = '"+Class[i]+"'"
                                UserID_array = Select_SQL(sql)
                                UserID = UserID_array[0][0]
                                if UserID != 'none':
                                    Line_Post(text,UserID)
                            Status = 'Send'
                    except Exception as e:
                        sql = "insert into SystemLog(PageName,PageFunc,PageLog,EX)values('python','Check_Late_Student','Check_Late_Student','"+str(e)+"')"
                        Insert_SQL(sql)
        else:
            Status = ''

                
@app.route('/HikVision_Data',methods=['POST'])
def HikVision_Data():
    text = ''
    week = datetime.today().isoweekday()
    
    # today_date = datetime.today().strftime('%Y-%m-%d')
    # class_time = datetime.strptime((today_date + ' 08:15:00'),'%Y-%m-%d %H:%M:%S')
    # class_end_time = datetime.strptime((today_date + ' 17:50:00'),'%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    
    # data = request.get_data()  #All data to see this
    try:
        hikvision_event_log = request.form['event_log']
        print(hikvision_event_log)
    
        json_data = json.loads(hikvision_event_log)
        date_and_time = json_data['dateTime'][0:19]
        date = json_data['dateTime'][0:10]
        
        AccessControllerEvent = json_data['AccessControllerEvent']
        currentVerifyMode = AccessControllerEvent['currentVerifyMode']
    
        if currentVerifyMode != 'invalid':
            if 'name' in AccessControllerEvent:
                employeeNoString = AccessControllerEvent['employeeNoString'] #工號
                name = AccessControllerEvent['name']
                label = AccessControllerEvent['label'] #考勤設置
                       
                # sql = "select Name FROM [KarlSchool].[dbo].[FaceRecognition_Log] where Number='"+employeeNoString+"' and Create_Date = '"+date+"' and Class_Status = 'in class'"
                # check = Select_SQL(sql)
                if label == 'Class':
                    # sql = "select a.UserID FROM [KarlSchool].[dbo].[Class_List] a left join [KarlSchool].[dbo].[Person_List] b on a.Class_Name = b.Class where Serial_Number='"+employeeNoString+"'"
                    # UserID_array = Select_SQL(sql)
                    # UserID = ''
                    # if len(UserID_array) != 0:
                    #     UserID = UserID_array[0][0]
                    #     print(UserID)
                    #     if not UserID is None:
                            # if now > class_time:
                            #     text = name + ' be late in class   ' + now.strftime('%Y-%m-%d %H:%M:%S')
                            # else:
                    text = name + ' in class   ' + now.strftime('%Y-%m-%d %H:%M:%S')
                            #Line_Post(text,UserID)
                    sql = "select Parent_UserID FROM [KarlSchool].[dbo].[Person_List] where Serial_Number = '"+employeeNoString+"'"
                    Parent_UserID = Select_SQL(sql)
                    if Parent_UserID[0][0] != '':
                        Line_Post(text,Parent_UserID[0][0])
                    text = ''
                    sql = "insert into [dbo].[FaceRecognition_Log](Name,Number,Create_Datetime,Create_Date,Week,Class_Status)values('{}','{}','{}','{}','{}','{}')".format(name,employeeNoString,date_and_time,date,week,'Class')
                    Insert_SQL(sql)
                elif label == 'Rest':
                    # sql = "select a.UserID FROM [KarlSchool].[dbo].[Class_List] a left join [KarlSchool].[dbo].[Person_List] b on a.Class_Name = b.Class where Serial_Number='"+employeeNoString+"'"
                    # UserID_array = Select_SQL(sql)
                    # UserID = ''
                    # if len(UserID_array) != 0:
                    #     UserID = UserID_array[0][0]
                    #     print(UserID)
                    #     if not UserID is None:
                            # if now < class_end_time:
                            #     text = name + ',class dismissed early  ' + now.strftime('%Y-%m-%d %H:%M:%S')
                            # else:
                    text = name + ',class dismissed   ' + now.strftime('%Y-%m-%d %H:%M:%S')
                    #Line_Post(text,UserID)
                    sql = "select Parent_UserID FROM [KarlSchool].[dbo].[Person_List] where Serial_Number = '"+employeeNoString+"'"
                    Parent_UserID = Select_SQL(sql)
                    if Parent_UserID[0][0] != '':
                        Line_Post(text,Parent_UserID[0][0])
                    text = ''
                    sql = "insert into [dbo].[FaceRecognition_Log](Name,Number,Create_Datetime,Create_Date,Week,Class_Status)values('{}','{}','{}','{}','{}','{}')".format(name,employeeNoString,date_and_time,date,week,'Rest')
                    Insert_SQL(sql)
                # else:
                #     sql = "insert into [dbo].[FaceRecognition_Log](Name,Number,Create_Datetime,Create_Date,Week,Class_Status)values('{}','{}','{}','{}','{}','{}')".format(name,employeeNoString,date_and_time,date,week,'')
                #     Insert_SQL(sql)
    except Exception as e:
        sql = "insert into SystemLog(PageName,PageFunc,PageLog,EX)values('python','HikVision_Data','HikVision_Data','"+str(e)+"')"
        Insert_SQL(sql)
    finally:
        result = {'a': 'b'}
        return result, 200

def app_run():
    app.run(host='10.1.1.59', port=5008)

if __name__ == "__main__": 
    threading.Thread(target=app_run).start()
    threading.Thread(target=Create_Put_Face_To_Device).start()
    threading.Thread(target=Check_Late_Student).start()