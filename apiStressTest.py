import os
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import json
import bcrypt
from datetime import datetime, timedelta, timezone
import threading
import time

current_time = datetime.now()
nowFormat = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
# # 加上一分钟
# next_minute = current_time + timedelta(minutes=2)
# # 转换为指定的字符串格式（YYYY-mm-dd HH:MM）
# formatted_time = next_minute.strftime('%Y-%m-%d %H:%M')

key = "hk4ljloyky2ng5v0wsaewkfekajw9x4w".encode("utf-8")
iv = "ql2tzupgy31fq8yq".encode("utf-8")
url = "https://pkappapi-lh42b6s57q-de.a.run.app/api/v1"
# url = "http://localhost:8080/api/v1"
apikey = "nxl9pzfolew3mli9"  # card
voucherkey = ""
apiver = "1"
over = "13"
appVersion = "3.2.40"

file_path = ""
randomize = "ZxxxEXcRPCq7vquKUC11cMWJ37UYGfn7VkXPBS5FAX9Cohhn8BKLYwvqvc5TmvKe"
devicecode = ""
accesstoken = ""
def deviceRegAndLogin1():
    global randomize, file_path, devicecode, accesstoken
    current_time = datetime.now()
    nowFormat = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
    # text_content = str([nowFormat]) + "  帳號1裝置註冊和登入開始\n"
    # with open(file_path, 'a') as file:
    # file.write(text_content)
    # print(text_content)

    data = json.dumps({"clientType": 0, "randomize": randomize}).encode("UTF-8")

    cipher = AES.new(key, AES.MODE_CBC, iv)

    cipheredData = cipher.encrypt(pad(data, AES.block_size))

    bData = b64encode(cipheredData).decode("UTF-8")
    # print(bData)
    postJson = {
        "data": bData,
        "apikey": apikey,
        "apiver": apiver,
        "over": over,
        "appVersion": appVersion,
    }
    # print(postJson)
    register = url + "/device/register"
    r = requests.post(register, data=postJson)
    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")
    # print(originalData)

    devicecode = json.loads(originalData)["data"]["devicecode"]
    # print(devicecode)

    # ================================================================
    # Login
    # ================================================================
    data = json.dumps(
        {
            "clientType": 0,
            "randomize": randomize,
            "email": "0961512578",
            "password": "a123456789",
        }
    ).encode("UTF-8")

    cipher = AES.new(key, AES.MODE_CBC, iv)

    cipheredData = cipher.encrypt(pad(data, AES.block_size))

    bData = b64encode(cipheredData).decode("UTF-8")

    postJson = {
        "data": bData,
        "devicecode": devicecode,
        "randomize": randomize,
        "devicetoken": "",
        "apikey": apikey,
        "apiver": apiver,
        "over": over,
        "appVersion": appVersion,
    }
    # print(postJson)
    login = url + "/member/login"
    r = requests.post(login, data=postJson)
    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")
    accesstoken = json.loads(originalData)["data"]["accesstoken"]
    # print(accesstoken)

    current_time = datetime.now()
    nowFormat2 = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
    # text_content_end = str([nowFormat2]) + "  帳號1裝置註冊和登入結束\n"
    # with open(file_path, 'a') as file:
    # file.write(text_content_end)
    # print(text_content_end)
    
    
def getMainPgae(thread_ID):
    global file_path
    # ================================================================
    # MainPage - banner
    # ================================================================
    current_time = datetime.now()
    nowFormat1 = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
   
    data = json.dumps(
        {
            "timestamp": 0,
        }
    ).encode("UTF-8")

    cipher = AES.new(key, AES.MODE_CBC, iv)

    cipheredData = cipher.encrypt(pad(data, AES.block_size))

    bData = b64encode(cipheredData).decode("UTF-8")

    postJson = {
        "data": bData,
        "devicecode": devicecode,
        "devicetoken": "",
        "accesstoken": accesstoken,
        "randomize": randomize,
        "devicetoken": "",
        "apikey": apikey,
        "apiver": apiver,
        "over": over,
        "appVersion": appVersion,
    }
    # print(postJson)
    newUrl = url + "/banners/list"
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")

    print("originalData:",originalData)
    current_time = datetime.now()
    nowFormat2 = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
   
    time1 = datetime.strptime(nowFormat1, "%Y-%m-%d %H-%M-%S-%f")
    time2 = datetime.strptime(nowFormat2, "%Y-%m-%d %H-%M-%S-%f")

    # 计算时间差
    time_difference = time2 - time1
    print("時間差:"+str(time_difference.total_seconds()))
deviceRegAndLogin1()

lock = threading.Lock()

running = True


def getMainPgaeThread1(thread_ID):
    global running
    while running:
        getMainPgae(thread_ID)
def read_thread_count_from_config(config_file):
    with open(config_file, "r") as file:
        for line in file:
            if line.strip() and line.startswith("threads"):
                parameter_name, parameter_value = line.strip().split("=")
                if parameter_name.strip() == "threads":
                    try:
                        return int(parameter_value.strip())
                    except ValueError:
                        return 0
    return 0


thread_count = read_thread_count_from_config("config.txt")
# 创建并启动线程
threads = []
for i in range(1, thread_count + 1):
    thread1 = threading.Thread(target=getMainPgaeThread1, args=(i,))
    threads.append(thread1)
    thread1.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

# 主线程等待用户输入以停止线程
# input("按Enter键停止執行續...")
running = False  # 设置标志以停止线程
for thread in threads:
    thread.join()

print("執行續已停止")