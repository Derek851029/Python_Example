import cv2
import numpy as np
import os
import socket

    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.2.63', 1884))
s.listen()

while True:
    conn, addr = s.accept()						# Wait for client connecting...(Blocking)
    print('************************************************************************')
    print(conn,addr)
    print('************************************************************************')