# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 16:55:17 2021

@author: Acme
"""


from websocket_server import WebsocketServer
import threading,cv2,base64,time
import socket
import requests
from flask import Flask, current_app, request, Response
from flask_cors import CORS
import datetime
import pyodbc
import json

app = Flask(__name__)
CORS(app)

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sever_ip = "192.168.2.81"
port2 = 5000

action = ""
practice_time = 0
Location = ""
action_code = ""
Case_Number = ""
Type = ""
SYSID = ""
req_age = ""
req_sex = ""

test_time = 30
INrectangle = ""

reciprocal = "standby"
reciprocal_endtime = datetime.datetime.now() + datetime.timedelta(seconds=10000000)

last_time = datetime.datetime.now() + datetime.timedelta(seconds=10000000)
end_time = datetime.datetime.now()
Test_start = ""
Send_Action = ""
INrectangle = ""
test_end = ""
Send_end = ""

camera1 = None
frame = cv2.imread('1.jpg', cv2.IMREAD_COLOR)
# rtsp_path = 'rtsp://192.168.2.195:5500/camera'
rtsp_path = 'rtsp://derekfang1029@gmail.com:jan60000@192.168.2.164/live/video_audio/profile1'


def new_client(client,server):
    global Send_end
    print('Client(%d) has joined.' % client['id'])
    Send_end = ""
    

def client_left(client,server):
    print('Client(%d) disconnected ' % client['id'])
    
    
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200]+'..'
    print('Client(%d) said: %s ' %(client['id'], message))
    global camera1
    #camera1 = cv2.VideoCapture(message)
    # client['rtsp'] = 'rtsp://192.168.2.195:5500/camera'
    # client['camera'] = cv2.VideoCapture('rtsp://192.168.2.195:5500/camera')
    client['rtsp'] = 'rtsp://derekfang1029@gmail.com:jan60000@192.168.2.164/live/video_audio/profile1'
    client['camera'] = cv2.VideoCapture('rtsp://derekfang1029@gmail.com:jan60000@192.168.2.164/live/video_audio/profile1')
    # client['rtsp'] = message
    # client['camera'] = cv2.VideoCapture(message)


def message_back(client,server,message):
    # 这里的message参数就是客户端传进来的内容
    print("Client(%d) said: %s" % (client['id'], message))
    # 这里可以对message进行各种处理
    result = "服务器已经收到消息了..." + message
    # 将处理后的数据再返回给客户端
    server.send_message(client, result)


def from_vedio():
    thread1 = threading.Thread(target=vedio_thread1, args=(1,))
    thread1.start()
    thread2 = threading.Thread(target=vedio_thread2, args=(1,))
    thread2.start()
    thread3 = threading.Thread(target=Wait_Socket)
    thread3.start()
    print('start')


def vedio_thread1(n):
    global INrectangle,test_end,Send_Action, Send_end,action
    
    while True:
        for i in server.clients:
            if 'frame' not in i.keys():
                continue
            frame = cv2.resize(i['frame'],(1500,700))
            cv2.rectangle(frame,(490,30),(1000,700),(0,255,0),2)
            #cv2.rectangle(frame,(660,80),(1250,950),(0,255,0),2) 原圖方框
            image = cv2.imencode('.jpg', frame)[1]
            base64_data = base64.b64encode(image)
            s = base64_data.decode()
            try:
                #send給web
                if Send_end == "OK":
                    Send = {'Data':str(s),'Message':'測驗結束'}
                    server.send_message(i,str(Send))
                else:
                    Message = Check_time()
                    Send = {'Data':str(s),'Message':Message}
                    server.send_message(i,str(Send))

                #send給server
                compression_frame = frame[30:700, 490:1000]
                ret, jpeg = cv2.imencode('.jpg', compression_frame)
                data = jpeg.tobytes()
                if test_end == "YES":
                    client.send((str(len(data)).ljust(16)).encode())
                    client.send(data)
                    client.send((str(len("Last")).ljust(16)).encode())
                    client.send("Last".encode())
                    Send_end = "OK"
                    test_end = ""
                else:
                    client.send((str(len(data)).ljust(16)).encode())
                    client.send(data)
                    if Send_Action == "Send":
                        client.send((str(len(action)).ljust(16)).encode())
                        client.send(action.encode())
                        Send_Action = ""
            except Exception as ex:
                print(ex)
        time.sleep(0.05)


def vedio_thread2(n):
    global camera1
    # camera1 = cv2.VideoCapture(0)
    global frame
    while True:
        for i in server.clients:
            if 'rtsp' not in i.keys():
                continue
            if 'camera' not in i.keys():
                i['camera'] = cv2.VideoCapture(i['rtsp'])
                continue
            ret, img_bgr = i['camera'].read()
            if img_bgr is None:
                #i['camera'] = cv2.VideoCapture(i['rtsp'])
                print('丟失幀')
            else:
                i['frame'] = img_bgr

def Check_time():
    global reciprocal,end_time,last_time,reciprocal_endtime,test_end,action,INrectangle,Test_start,Send_Action,Type
    if reciprocal == "Calculating_time":
        reciprocal_endtime = datetime.datetime.now() + datetime.timedelta(seconds=6)
        reciprocal = "Start"

    if reciprocal == "Start":
        last_time = reciprocal_endtime - datetime.datetime.now()
        if last_time.seconds <= 3:
            if last_time.seconds == 0:
                reciprocal = ""
            else:
                return str(last_time.seconds)

        else:
            return "請勿移動，三秒後開始測驗"

    #上面倒數三秒, 下面是正式測驗秒數
    if (reciprocal_endtime - datetime.datetime.now()).seconds == 0: #先執行()中, 在取得秒數
        reciprocal_endtime = datetime.datetime.now() + datetime.timedelta(seconds=100000) #怕上面再次執行到if, 把時間拉到無限大

        end_time = datetime.datetime.now() + datetime.timedelta(seconds=test_time)
        Test_start = "Start"
        Send_Action = "Send"

    if Test_start == "Start":
        last_time = end_time - datetime.datetime.now()
        if last_time.seconds == 0:
            Test_start = ""
            test_end = "YES"
            return "0"
        else:
            if last_time.seconds > 5:
                return "測驗開始"
            else:
                return str(last_time.seconds)
    else:
        tk_text = "請站入方框內" #更改變數text中的text參數

    if INrectangle == "YES":
        INrectangle = ""
        tk_text = "請勿移動，三秒後開始測驗"
        reciprocal = "Calculating_time"
    return tk_text

def Wait_Socket():
    global Case_Number, Type, SYSID, req_age, req_sex, action, action_code, Location, INrectangle,test_end

    while True:
        server_recv = str(client.recv(1024),encoding="utf-8")
        print(server_recv)
        if server_recv == "YES":
            INrectangle = "YES"
        elif server_recv.isdigit() == True:
            test_end = "End"
            print(req_sex)
            print(server_recv)
            print(action)
            test_score = Score(str(server_recv),req_age,action,req_sex)
            sql = "INSERT INTO [dbo].[Evaluation_Result] (Case_Number, Action, Type, Location, Score, SYSID,ActionTimes) VALUES ('{}', '{}', '{}', '{}', '{}', '{}','{}')".format(Case_Number,action_code,Type,Location,test_score,SYSID,server_recv)
            InsertSQL(sql)
        elif '.' in str(server_recv):
            test_end = "End"
            server_recv = str(server_recv)[0:2]
            if action == "Extend_Chest":
                action = "荷重擴胸"
            elif action == "Front_External_Lift_Shoulder":
                action = "前側外側抬肩"
            elif action == "Split_Squat":
                action = "分腿蹲"
            elif action == "Squat_Wall_Hold":
                action = "靠牆蹲"
            sql = "INSERT INTO [dbo].[Evaluation_Result] (Case_Number, Action, Type, Score, SYSID) VALUES ('{}', '{}', '{}', '{}', '{}')".format(Case_Number, action, Type, server_recv, SYSID)
            InsertSQL(sql)

def Score(total,age,action,sex):
    if sex == "男":
        if action == "Stand_Sit":
            if int(age) >=65 and int(age) < 70:
                if int(total) >= 12 and int(total) < 14:
                    return "1"
                elif int(total) >= 14 and int(total) < 17:
                    return "2"
                elif int(total) >= 17 and int(total) <20:
                    return "3"
                elif int(total) >= 20 and int(total) < 23:
                    return "4"
                elif int(total) >= 23:
                    return "5"
                else:
                    return "0"
            elif int(age) >=70 and int(age) < 75:
                if int(total) >= 10 and int(total) < 13:
                    return "1"
                elif int(total) >= 13 and int(total) < 16:
                    return "2"
                elif int(total) >= 16 and int(total) < 18:
                    return "3"
                elif int(total) >= 18 and int(total) < 20:
                    return "4"
                elif int(total) >= 20:
                    return "5"
                else:
                    return "0"
            elif int(age) >=75 and int(age) < 80:
                if int(total) >= 9 and int(total) < 11:
                    return "1"
                elif int(total) >= 11 and int(total) < 14:
                    return "2"
                elif int(total) == 14 and int(total) < 18:
                    return "3"
                elif int(total) >= 18 and int(total) < 20:
                    return "4"
                elif int(total) >= 20:
                    return "5"
                else:
                    return "0"
            elif int(age) >=80 and int(age) < 85:
                if int(total) >= 7 and int(total) < 10:
                    return "1"
                elif int(total) >= 10 and int(total) < 13:
                    return "2"
                elif int(total) >= 13 and int(total) < 16:
                    return "3"
                elif int(total) >= 16 and int(total) < 18:
                    return "4"
                elif int(total) >= 18:
                    return "5"
                else:
                    return "0"
            elif int(age) >=85 and int(age) < 90:
                if int(total) >= 4 and int(total) < 7:
                    return "1"
                elif int(total) >= 7 and int(total) < 11:
                    return "2"
                elif int(total) >= 11 and int(total) < 13:
                    return "3"
                elif int(total) >= 13 and int(total) < 15:
                    return "4"
                elif int(total) >= 15:
                    return "5"
                else:
                    return "0"
            elif int(age) >=90:
                if int(total) >= 3 and int(total) < 6:
                    return "1"
                elif int(total) >= 6 and int(total) < 7:
                    return "2"
                elif int(total) >= 7 and int(total) < 11:
                    return "3"
                elif int(total) >= 11 and int(total) < 13:
                    return "4"
                elif int(total) >= 13:
                    return "5"
                else:
                    return "0"
        if action == "Lift_Dumbell":
            if int(age) >=65 and int(age) < 70:
                if int(total) >= 13 and int(total) < 16:
                    return "1"
                elif int(total) >= 16 and int(total) < 19:
                    return "2"
                elif int(total) >= 19 and int(total) < 20:
                    return "3"
                elif int(total) >= 20 and int(total) < 23:
                    return "4"
                elif int(total) >= 23:
                    return "5"
                else:
                    return "0"
            elif int(age) >=70 and int(age) < 75:
                if int(total) >= 13 and int(total) < 15:
                    return "1"
                elif int(total) >= 15 and int(total) < 18:
                    return "2"
                elif int(total) >= 18 and int(total) < 19:
                    return "3"
                elif int(total) >= 19 and int(total) < 22:
                    return "4"
                elif int(total) >= 22:
                    return "5"
                else:
                    return "0"
            elif int(age) >=75 and int(age) < 80:
                if int(total) >= 10 and int(total) < 14:
                    return "1"
                elif int(total) >= 14 and int(total) < 16:
                    return "2"
                elif int(total) >= 16 and int(total) < 18:
                    return "3"
                elif int(total) >= 18 and int(total) < 20:
                    return "4"
                elif int(total) >= 20:
                    return "5"
                else:
                    return "0"
            elif int(age) >=80 and int(age) < 85:
                if int(total) >= 10 and int(total) < 13:
                    return "1"
                elif int(total) >= 13 and int(total) < 16:
                    return "2"
                elif int(total) >= 16 and int(total) < 18:
                    return "3"
                elif int(total) >= 18 and int(total) < 20:
                    return "4"
                elif int(total) >= 20:
                    return "5"
                else:
                    return "0"
            elif int(age) >=85 and int(age) < 90:
                if int(total) >= 5 and int(total) < 10:
                    return "1"
                elif int(total) >= 10 and int(total) < 14:
                    return "2"
                elif int(total) >= 14 and int(total) < 16:
                    return "3"
                elif int(total) >= 16 and int(total) < 17:
                    return "4"
                elif int(total) >= 17:
                    return "5"
                else:
                    return "0"
            elif int(age) >=90:
                if int(total) >= 5 and int(total) < 10:
                    return "1"
                elif int(total) >= 10 and int(total) < 12:
                    return "2"
                elif int(total) >= 12 and int(total) < 14:
                    return "3"
                elif int(total) >= 14 and int(total) < 17:
                    return "4"
                elif int(total) >= 17:
                    return "5"
                else:
                    return "0"
        if action == "原地站立抬膝":
            if int(age) >=65 and int(age) < 70:
                if int(total) >= 72  and int(total) <=89:
                    return "1"
                elif int(total) == 90 or int(total) == 91 or int(total) == 96:
                    return "2"
                elif int(total) >=97 and int(total) <= 105:
                    return "3"
                elif int(total) == 106 or int(total) == 107 or int(total) == 108 or int(total) == 109:
                    return "4"
                elif int(total) >= 110:
                    return "5"
                else:
                    return "0"
            elif int(age) >=70 and int(age) < 75:
                if int(total) >= 53  and int(total) < 81:
                    return "1"
                elif int(total) >= 81 and int(total) < 92:
                    return "2"
                elif int(total) >=92 and int(total) < 103:
                    return "3"
                elif int(total) >=103 and int(total) < 110:
                    return "4"
                elif int(total) >= 110:
                    return "5"
                else:
                    return "0"
            elif int(age) >=75 and int(age) < 80:
                if int(total) >= 51  and int(total) < 77:
                    return "1"
                elif int(total) >= 77 and int(total) < 95:
                    return "2"
                elif int(total) >=95 and int(total) < 102:
                    return "3"
                elif int(total) >=102 and int(total) < 106:
                    return "4"
                elif int(total) >= 106:
                    return "5"
                else:
                    return "0"
            elif int(age) >=80 and int(age) < 85:
                if int(total) >= 32  and int(total) < 78:
                    return "1"
                elif int(total) >= 78 and int(total) < 91:
                    return "2"
                elif int(total) >=91 and int(total) < 99:
                    return "3"
                elif int(total) >=99 and int(total) < 103:
                    return "4"
                elif int(total) >= 103:
                    return "5"
                else:
                    return "0"
            elif int(age) >=85 and int(age) < 90:
                if int(total) >= 31  and int(total) < 60:
                    return "1"
                elif int(total) >= 60 and int(total) < 80:
                    return "2"
                elif int(total) >=80 and int(total) < 94:
                    return "3"
                elif int(total) >=94 and int(total) < 103:
                    return "4"
                elif int(total) >= 103:
                    return "5"
                else:
                    return "0"
            elif int(age) >=90:
                if int(total) >= 31  and int(total) < 53:
                    return "1"
                elif int(total) >= 53 and int(total) < 70:
                    return "2"
                elif int(total) >=70 and int(total) < 85:
                    return "3"
                elif int(total) >=85 and int(total) < 91:
                    return "4"
                elif int(total) >= 91:
                    return "5"
                else:
                    return "0"
    elif sex == "女":
        if action == "椅子坐立":
            if int(age) >=65 and int(age) < 70:
                if int(total) >= 9  and int(total) < 14:
                    return "1"
                elif int(total) >= 14 and int(total) < 17:
                    return "2"
                elif int(total) >=17 and int(total) < 18:
                    return "3"
                elif int(total) >=18 and int(total) < 20:
                    return "4"
                elif int(total) >= 20:
                    return "5"
                else:
                    return "0"
            elif int(age) >=70 and int(age) < 75:
                if int(total) >= 9  and int(total) < 13:
                    return "1"
                elif int(total) >= 13 and int(total) < 15:
                    return "2"
                elif int(total) >=15 and int(total) < 17:
                    return "3"
                elif int(total) >=17 and int(total) < 19:
                    return "4"
                elif int(total) >= 19:
                    return "5"
                else:
                    return "0"
            elif int(age) >=75 and int(age) < 80:
                if int(total) >= 6  and int(total) < 11:
                    return "1"
                elif int(total) >= 11 and int(total) < 14:
                    return "2"
                elif int(total) >=14 and int(total) < 17:
                    return "3"
                elif int(total) >=17 and int(total) < 18:
                    return "4"
                elif int(total) >= 18:
                    return "5"
                else:
                    return "0"
            elif int(age) >=80 and int(age) < 85:
                if int(total) >= 6  and int(total) < 8:
                    return "1"
                elif int(total) >= 8 and int(total) < 10:
                    return "2"
                elif int(total) >=10 and int(total) < 13:
                    return "3"
                elif int(total) >=13 and int(total) < 15:
                    return "4"
                elif int(total) >= 15:
                    return "5"
                else:
                    return "0"
            elif int(age) >=85 and int(age) < 90:
                if int(total) >= 4  and int(total) < 7:
                    return "1"
                elif int(total) >= 7 and int(total) < 10:
                    return "2"
                elif int(total) >=10 and int(total) < 11:
                    return "3"
                elif int(total) >=11 and int(total) < 14:
                    return "4"
                elif int(total) >= 14:
                    return "5"
                else:
                    return "0"
            elif int(age) >=90:
                if int(total) >= 4  and int(total) < 5:
                    return "1"
                elif int(total) >= 5 and int(total) < 8:
                    return "2"
                elif int(total) >=8 and int(total) < 11:
                    return "3"
                elif int(total) >=11 and int(total) < 12:
                    return "4"
                elif int(total) >= 12:
                    return "5"
                else:
                    return "0"
        if action == "肱二頭肌手臂屈舉":
            if int(age) >=65 and int(age) < 70:
                if int(total) >= 10  and int(total) < 14:
                    return "1"
                elif int(total) >= 14 and int(total) < 16:
                    return "2"
                elif int(total) >=16 and int(total) < 19:
                    return "3"
                elif int(total) >=19 and int(total) < 20:
                    return "4"
                elif int(total) >= 20:
                    return "5"
                else:
                    return "0"
            elif int(age) >=70 and int(age) < 75:
                if int(total) >= 10  and int(total) < 14:
                    return "1"
                elif int(total) >= 14 and int(total) < 15:
                    return "2"
                elif int(total) >= 15 and int(total) < 18:
                    return "3"
                elif int(total) >=18 and int(total) < 20:
                    return "4"
                elif int(total) >= 20:
                    return "5"
                else:
                    return "0"
            elif int(age) >=75 and int(age) < 80:
                if int(total) >= 8  and int(total) < 13:
                    return "1"
                elif int(total) >= 13 and int(total) < 15:
                    return "2"
                elif int(total) >=15 and int(total) < 18:
                    return "3"
                elif int(total) >=18 and int(total) < 20:
                    return "4"
                elif int(total) >= 20:
                    return "5"
                else:
                    return "0"
            elif int(age) >=80 and int(age) < 85:
                if int(total) >= 5  and int(total) < 10:
                    return "1"
                elif int(total) >= 10 and int(total) < 12:
                    return "2"
                elif int(total) >=12 and int(total) < 16:
                    return "3"
                elif int(total) >=16 and int(total) < 17:
                    return "4"
                elif int(total) >= 17:
                    return "5"
                else:
                    return "0"
            elif int(age) >=85 and int(age) < 90:
                if int(total) >= 4  and int(total) < 9:
                    return "1"
                elif int(total) >= 9 and int(total) < 13:
                    return "2"
                elif int(total) >=13 and int(total) < 15:
                    return "3"
                elif int(total) >=15 and int(total) < 17:
                    return "4"
                elif int(total) >= 17:
                    return "5"
                else:
                    return "0"
            elif int(age) >=90:
                if int(total) >= 4  and int(total) < 5:
                    return "1"
                elif int(total) >= 5 and int(total) < 8:
                    return "2"
                elif int(total) >=8 and int(total) < 12:
                    return "3"
                elif int(total) >=12 and int(total) < 15:
                    return "4"
                elif int(total) >= 15:
                    return "5"
                else:
                    return "0"
        if action == "原地站立抬膝":
            if int(age) >=65 and int(age) < 70:
                if int(total) >= 69  and int(total) < 90:
                    return "1"
                elif int(total) >= 90 and int(total) < 100:
                    return "2"
                elif int(total) >=100 and int(total) < 106:
                    return "3"
                elif int(total) == 106 and int(total) < 113:
                    return "4"
                elif int(total) >= 113:
                    return "5"
                else:
                    return "0"
            elif int(age) >=70 and int(age) < 75:
                if int(total) >= 56  and int(total) < 80:
                    return "1"
                elif int(total) >= 80 and int(total) < 96:
                    return "2"
                elif int(total) >=96 and int(total) < 103:
                    return "3"
                elif int(total) >=103 and int(total) < 109:
                    return "4"
                elif int(total) >= 109:
                    return "5"
                else:
                    return "0"
            elif int(age) >=75 and int(age) < 80:
                if int(total) >= 50  and int(total) < 73:
                    return "1"
                elif int(total) >= 73 and int(total) < 90:
                    return "2"
                elif int(total) >=90 and int(total) < 100:
                    return "3"
                elif int(total) >=100 and int(total) < 106:
                    return "4"
                elif int(total) >= 106:
                    return "5"
                else:
                    return "0"
            elif int(age) >=80 and int(age) < 85:
                if int(total) >= 35  and int(total) < 57:
                    return "1"
                elif int(total) >= 57 and int(total) < 77:
                    return "2"
                elif int(total) >= 77 and int(total) < 87:
                    return "3"
                elif int(total) >= 87 and int(total) < 97:
                    return "4"
                elif int(total) >= 97:
                    return "5"
                else:
                    return "0"
            elif int(age) >=85 and int(age) < 90:
                if int(total) >= 36  and int(total) < 57:
                    return "1"
                elif int(total) >= 57 and int(total) < 76:
                    return "2"
                elif int(total) >=76 and int(total) < 90:
                    return "3"
                elif int(total) >=90 and int(total) < 103:
                    return "4"
                elif int(total) >= 103:
                    return "5"
                else:
                    return "0"
            elif int(age) >=90:
                if int(total) >= 30  and int(total) < 40:
                    return "1"
                elif int(total) >= 40 and int(total) < 57:
                    return "2"
                elif int(total) >=57 and int(total) < 81:
                    return "3"
                elif int(total) >=81 and int(total) < 90:
                    return "4"
                elif int(total) >= 90:
                    return "5"
                else:
                    return "0"

def InsertSQL(sql):
    conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=210.68.227.123,8585; DATABASE=Veterans_CRM; UID=sa; PWD=Acme-70472615')
    cursor = conn.cursor()
    sqlstr = sql
    cursor.execute(sqlstr)
    conn.commit()
    conn.close()
    return "success"

def TestTime(req_action):
    global Location, test_time, action_code, action, practice_time
    if req_action == "practice":
        test_time = int(practice_time)
        print(test_time)         
    elif req_action == "30秒椅子坐立":
        Location = "下肢"
        test_time = 30
        action = "Stand_Sit"
        action_code = "A"
    elif req_action == "30秒肱二頭肌手臂屈舉":
        Location = "上肢"
        test_time = 30
        action = "Lift_Dumbell"
        action_code = "B"

    elif req_action == "荷重擴胸":
        action = "Extend_Chest"
        test_time = 37
    elif req_action == "前側外側抬肩":
        action = "Front_External_Lift_Shoulder"
        test_time = 36
    elif req_action == "分腿蹲":
        action = "Split_Squat"
        test_time = 40
    elif req_action == "靠牆蹲":
        action = "Squat_Wall_Hold"
        test_time = 40

@app.route('/flask_client',methods=['POST'])
def Evaluation():
    global action, test_time, Post, Case_Number, Type, SYSID, req_age, req_sex,practice_time

    Post = "Post"
    #接JSON方式
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))

    practice_time = json_data.get("practice_time")
    action = json_data.get("action")
    Case_Number = json_data.get("Case_Number")
    Type = json_data.get("Type")
    SYSID = json_data.get("SYSID")
    req_age = json_data.get("Age")
    req_sex = json_data.get("Sex")

    print(action)
    TestTime(action)

    return ""

def app_run():
    app.run(host="192.168.2.81", port=5001)


# 新建一个WebsocketServer对象，第一个参数是端口号，第二个参数是host
# 如果host为空，则默认为本机IP
port = 8022
server = WebsocketServer(port, '0.0.0.0')

client.connect((sever_ip,port2))

from_vedio()

# 设置当有新客户端接入时的动作
server.set_fn_new_client(new_client)
# 设置当有客户端断开时的动作
server.set_fn_client_left(client_left)
# 设置当接收到某个客户端发送的消息后的操作
server.set_fn_message_received(message_received)

threading.Thread(target=app_run).start()
# 设置服务一直运行
server.run_forever()











