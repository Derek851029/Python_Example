# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 16:55:17 2021

@author: Acme
"""


from websocket_server import WebsocketServer
import threading,cv2,base64,time


camera1 = None
frame = cv2.imread('1.jpg', cv2.IMREAD_COLOR)
rtsp_path = 0
#rtsp_path = 'rtsp://derek850:jan60000@192.168.2.180/live/video_audio/profile1'


def new_client(client,server):
    print('Client(%d) has joined.' % client['id'])
    

def client_left(client,server):
    print('Client(%d) disconnected ' % client['id'])
    
    
def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200]+'..'
    print('Client(%d) said: %s ' %(client['id'], message))
    global camera1
    #camera1 = cv2.VideoCapture(message)
    client['rtsp'] = message
    client['camera'] = cv2.VideoCapture(message)


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
    print('start')


def vedio_thread1(n):
    print('send')
    while True:
        for i in server.clients:
            if 'frame' not in i.keys():
                continue
            image = cv2.imencode('.jpg', i['frame'])[1]
            base64_data = base64.b64encode(image)
            s = base64_data.decode()
            try:
                server.send_message(i,'data:image/jpeg;base64,%s' %s)
            except Exception as ex:
                print(ex)
        
            
        time.sleep(0.05)


def vedio_thread2(n):
    global camera1
    #camera1 = cv2.VideoCapture(rtsp_path)
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






# 新建一个WebsocketServer对象，第一个参数是端口号，第二个参数是host
# 如果host为空，则默认为本机IP
port = 8022
server = WebsocketServer(port, '0.0.0.0')

from_vedio()

# 设置当有新客户端接入时的动作
server.set_fn_new_client(new_client)
# 设置当有客户端断开时的动作
server.set_fn_client_left(client_left)
# 设置当接收到某个客户端发送的消息后的操作
server.set_fn_message_received(message_received)
# 设置服务一直运行
server.run_forever()









