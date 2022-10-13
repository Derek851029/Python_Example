import requests
import json
import pyodbc
from flask import Flask, current_app, request, Response
from flask_cors import CORS
# from firebase_admin import messaging
# import firebase_admin
# from firebase_admin import credentials

app = Flask(__name__)
CORS(app)

def Select_SQL(sql):
    conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=210.68.227.123,8585; DATABASE=DimaxCallcenter; UID=sa; PWD=Acme-70472615')
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

def Firebase_Send():
    return ""
    
@app.route('/Send_Notification',methods=['POST'])
def Send_Notification():
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))
    
    Type = json_data.get("type")
    
    if Type == 'Announce':
        Title = json_data.get("Title")
        Message = json_data.get("Message")
        Depart = json_data.get("Depart")
        Depart_arr = Depart.split(',')
        print(Depart_arr)
        for i in Depart_arr:
            sql = "SELECT SYSID FROM [dbo].[DispatchSystem] WHERE Agent_Status='在職' AND Agent_Team = '{}'".format(i)
            SYSID = Select_SQL(sql)
            print(SYSID)
            for x in SYSID: #the SYSID like [[SYSID],[SYSID]], so need two for
                for y in x:
                    print(y)
                    sql = "SELECT token FROM [dbo].[Device_token] WHERE Agent_SYSID = '{}'".format(y)
                    token = Select_SQL(sql)
                    if len(token) != 0:
                        for a in token:
                            for b in a:
                                print(b)
                                headers = {'Content-Type': 'application/json','Authorization':'key=AAAArRKfUys:APA91bHukMrJZlwJkctsPYlhxdMgA4sqTVcr5b5hw8Byj7aVGgJNOnKK6PkFdbDie00E3OvC-HiwJf1jOUdh8bMGRBsuWglXK-yMivpsQ0Aw-hf-qxtD16Z7bXDyxcDj45ZSsC9iyDSA'}
                                body = {
                                          'notification': {'title': Title,
                                                            'body': Message
                                                            },
                                          'to':b,
                                          'priority': 'high',
                                        }
                                
                                response = requests.post('https://fcm.googleapis.com/fcm/send',headers=headers, data=json.dumps(body))
                                print(response.status_code)
                                
                                print(response.json())
    
    
    if Type == 'Schedule':
        Visit_Customer = json_data.get("Visit_Customer")
        Visit_Date = json_data.get("Visit_Date")
        SYSID = json_data.get("SYSID")
        SYSID_arr = SYSID.split(',')
        
        for i in SYSID_arr:
            print(i)
            sql = "SELECT token FROM [dbo].[Device_token] WHERE Agent_SYSID = '{}'".format(i)
            token = Select_SQL(sql)
            print(token)
            if len(token) != 0:
                for x in token:
                    for y in x:
                        print(y)
                        headers = {'Content-Type': 'application/json','Authorization':'key=AAAArRKfUys:APA91bHukMrJZlwJkctsPYlhxdMgA4sqTVcr5b5hw8Byj7aVGgJNOnKK6PkFdbDie00E3OvC-HiwJf1jOUdh8bMGRBsuWglXK-yMivpsQ0Aw-hf-qxtD16Z7bXDyxcDj45ZSsC9iyDSA'}
                        body = {
                                  'notification': {'title': '行程公告',
                                                    'body': '拜訪客戶:'+Visit_Customer+'/拜訪時程:'+Visit_Date+''
                                                    },
                                  'to':y,
                                  'priority': 'high',
                                }
                        
                        response = requests.post('https://fcm.googleapis.com/fcm/send',headers=headers, data=json.dumps(body))
                        print(response.status_code)
                        
                        print(response.json())
    return "success"

#========================firebase聊天系統==================================
# cred = credentials.Certificate("C:/Users/acer/Downloads/apex-health-bce9d-firebase-adminsdk-30wlo-8135756ac4.json")
# firebase_admin.initialize_app(cred)

# registration_token = 'e2sRAGrKTQWpGjQsLupkke:APA91bHE7AD1H6ZoJa_FiTEhJ3ne6QJE4uSl2EbDFnD-jLAHhWzJfgz2tDC6ZI_0P5aWSXmVLmQ_5UH4G46HjkUH43j2enxbSginSn66yoWaay69d7JBm6HVPyiwM0bXZWX7fcx1f3-9'
# notification = 'AAAArRKfUys:APA91bHukMrJZlwJkctsPYlhxdMgA4sqTVcr5b5hw8Byj7aVGgJNOnKK6PkFdbDie00E3OvC-HiwJf1jOUdh8bMGRBsuWglXK-yMivpsQ0Aw-hf-qxtD16Z7bXDyxcDj45ZSsC9iyDSA'
# message = messaging.Message(
#     data={
#         'score': '850',
#         'time': '14:49',
#     },
#     token=registration_token,
#     notification=notification
#     )

# # Send a message to the device corresponding to the provided
# # registration token.
# response = messaging.send(message)
# # Response is a message ID string.
# print('Successfully sent message:', response)

if __name__ == "__main__": 
    app.run(host="192.168.2.227", port=5008)
