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
voucehrurl = "https://pkappapi-lh42b6s57q-de.a.run.app/pkvoucher/v1"

apikey = "nxl9pzfolew3mli9"  # card
voucherkey = ""
apiver = "1"
over = "13"
appVersion = "3.2.40"

file_path = ""
randomize = "ZxxxEXcRPCq7vquKUC11cMWJ37UYGfn7VkXPBS5FAX9Cohhn8BKLYwvqvc5TmvKe"
randomize2 = "yEmct2RgAceA84ZjMNKWocpmkJt2T96INLHKKoRDwkQWGY50HJUVCK9aNVYvKN1X"
devicecode = ""
devicecode2 = ""
accesstoken = ""
accesstoken2 = ""


def CreateFile():
    global file_path
    current_directory = os.getcwd()
    current_time = datetime.now()
    nowFormat = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]

    file_name = nowFormat + "帳號1登入.txt"
    file_name2 = nowFormat + "帳號2登入.txt"

    file_path = os.path.join(current_directory, file_name)
    # file_path = os.path.join(current_directory, file_name2)
    text_content = "建立記錄檔 開始測試\n"
    with open(file_path, "w") as file:
        file.write(text_content)
    # with open(file_path, 'w') as file:
    #     file.write(text_content)


# ====================================================
# 裝置註冊
# ====================================================
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
    print(accesstoken)

    current_time = datetime.now()
    nowFormat2 = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
    # text_content_end = str([nowFormat2]) + "  帳號1裝置註冊和登入結束\n"
    # with open(file_path, 'a') as file:
    # file.write(text_content_end)
    # print(text_content_end)


def deviceRegAndLogin2():
    global randomize2, file_path, devicecode2, accesstoken2

    current_time = datetime.now()
    nowFormat = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
    # text_content = str([nowFormat]) + "  帳號2裝置註冊和登入開始\n"
    # with open(file_path, 'a') as file:
    # file.write(text_content)
    # print(text_content)
    data = json.dumps({"clientType": 0, "randomize": randomize2}).encode("UTF-8")

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

    devicecode2 = json.loads(originalData)["data"]["devicecode"]
    # print(devicecode)

    # ================================================================
    # Login
    # ================================================================
    data = json.dumps(
        {
            "clientType": 0,
            "randomize": randomize,
            "email": "0931139959",
            "password": "44752964",
        }
    ).encode("UTF-8")

    cipher = AES.new(key, AES.MODE_CBC, iv)

    cipheredData = cipher.encrypt(pad(data, AES.block_size))

    bData = b64encode(cipheredData).decode("UTF-8")

    postJson = {
        "data": bData,
        "devicecode": devicecode2,
        "randomize": randomize2,
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
    accesstoken2 = json.loads(originalData)["data"]["accesstoken"]
    # print(accesstoken)

    current_time = datetime.now()
    nowFormat2 = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
    # text_content = str([nowFormat2]) + "  帳號2裝置註冊和登入結束\n"
    # with open(file_path, 'a') as file:
    # file.write(text_content)
    # print(text_content)


def getMainPgae(thread_ID):
    global file_path
    # ================================================================
    # MainPage - redeemablecouponlist
    # ================================================================
    current_time = datetime.now()
    nowFormat1 = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
    # text_content = str([nowFormat1]) + "執行續編號:" +str(thread_ID) + "  帳號1獲取首頁資訊開始\n"
    # with open(file_path, 'a') as file:
    # file.write(text_content)
    # print(text_content)
    data = json.dumps(
        {
            "clientType": 0,
            "brand": "kfc",
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
    newUrl = url + "/points/redeemablecouponlist"
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")

    # ================================================================
    # MainPage - coupon
    # ================================================================
    data = json.dumps(
        {
            "clientType": 0,
            "brand": "kfc",
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
    newUrl = url + "/coupon/list"
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")

    # ================================================================
    # MainPage - getPersonal
    # ================================================================
    data = json.dumps(
        {
            "clientType": 0,
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
    newUrl = url + "/mainpage/getPersonal"
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")

    # ================================================================
    # MainPage - getStrollet
    # ================================================================
    data = json.dumps(
        {
            "clientType": 0,
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
    newUrl = url + "/mainpage/getStrollet"
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")

    # ================================================================
    # MainPage - listNewsExtends
    # ================================================================
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
    newUrl = url + "/news/listNewsExtends"
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")

    # ================================================================
    # MainPage - mainpage/totalData
    # ================================================================
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
    newUrl = url + "/mainpage/totalData"
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")

    # ================================================================
    # MainPage - /favhislist/list - 我的最愛
    # ================================================================
    data = json.dumps(
        {
            "Fun": "fav",
            "member_id": "492426284",
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
    newUrl = (
        "https://pkappapi-lh42b6s57q-de.a.run.app/pkvoucher/v1/voucher/favhislist/list"
    )
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")

    # ================================================================
    # MainPage - /favhislist/list -再次訂購
    # ================================================================
    data = json.dumps(
        {
            "Fun": "ohlist",
            "member_id": "492426284",
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
    newUrl = (
        "https://pkappapi-lh42b6s57q-de.a.run.app/pkvoucher/v1/voucher/favhislist/list"
    )
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")
    print("favhislist:",originalData)
    current_time = datetime.now()
    nowFormat2 = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
    # text_content = str([nowFormat2]) + "執行續編號:" +str(thread_ID) +"  帳號1獲取首頁資訊結束\n"
    # print(text_content)
    time1 = datetime.strptime(nowFormat1, "%Y-%m-%d %H-%M-%S-%f")
    time2 = datetime.strptime(nowFormat2, "%Y-%m-%d %H-%M-%S-%f")

    # 计算时间差
    time_difference = time2 - time1
    with open(file_path, "a") as file:
        # file.write(text_content)
        # file.write("執行續編號:" +str(thread_ID) +"帳號1獲取首頁資訊結束-開始時間相差" + str(time_difference.total_seconds()) + "\n")
        file.write(str(time_difference.total_seconds()) + "\n")
        # file.write("----------------------------------------------------------\n")


def getMainPgae2(thread_ID):
    global file_path
    # ================================================================
    # MainPage - redeemablecouponlist
    # ================================================================
    current_time = datetime.now()
    nowFormat1 = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
    # text_content = str([nowFormat1]) + "執行續編號:" +str(thread_ID) + "  帳號2獲取首頁資訊開始\n"
    # with open(file_path, 'a') as file:
    #   file.write(text_content)
    # print(text_content)
    data = json.dumps(
        {
            "clientType": 0,
            "brand": "kfc",
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
    newUrl = url + "/points/redeemablecouponlist"
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")

    # ================================================================
    # MainPage - coupon
    # ================================================================
    data = json.dumps(
        {
            "clientType": 0,
            "brand": "kfc",
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
    newUrl = url + "/coupon/list"
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")

    # ================================================================
    # MainPage - getPersonal
    # ================================================================
    data = json.dumps(
        {
            "clientType": 0,
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
    newUrl = url + "/mainpage/getPersonal"
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")

    # ================================================================
    # MainPage - getStrollet
    # ================================================================
    data = json.dumps(
        {
            "clientType": 0,
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
    newUrl = url + "/mainpage/getStrollet"
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")

    # ================================================================
    # MainPage - listNewsExtends
    # ================================================================
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
    newUrl = url + "/news/listNewsExtends"
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")

    # ================================================================
    # MainPage - mainpage/totalData
    # ================================================================
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
    newUrl = url + "/mainpage/totalData"
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")

    # ================================================================
    # MainPage - /favhislist/list - 我的最愛
    # ================================================================
    data = json.dumps(
        {
            "Fun": "fav",
            "member_id": "492426284",
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
    newUrl = (
        "https://pkappapi-lh42b6s57q-de.a.run.app/pkvoucher/v1/voucher/favhislist/list"
    )
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")
    
    # ================================================================
    # MainPage - /favhislist/list -再次訂購
    # ================================================================
    data = json.dumps(
        {
            "Fun": "ohlist",
            "member_id": "492426284",
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
    newUrl = (
        "https://pkappapi-lh42b6s57q-de.a.run.app/pkvoucher/v1/voucher/favhislist/list"
    )
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")
    print("favhislist:",originalData)
    current_time = datetime.now()
    nowFormat2 = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
    # text_content = str([nowFormat2]) + "執行續編號:" +str(thread_ID) + "  帳號2獲取首頁資訊結束\n"
    # print(text_content)
    time1 = datetime.strptime(nowFormat1, "%Y-%m-%d %H-%M-%S-%f")
    time2 = datetime.strptime(nowFormat2, "%Y-%m-%d %H-%M-%S-%f")

    # 计算时间差
    time_difference = time2 - time1

    with open(file_path, "a") as file:
        # file.write(text_content)
        # file.write("執行續編號:" +str(thread_ID) +"帳號2獲取首頁資訊結束-開始時間相差" + str(time_difference.total_seconds()) + "\n")
        file.write(str(time_difference.total_seconds()) + "\n")
        # file.write("----------------------------------------------------------\n")


def getVoucher(thread_ID):
    # ================================================================
    # voucher - listProducts
    # ================================================================
    current_time = datetime.now()
    nowFormat1 = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
    text_content = (
        str([nowFormat1]) + "執行續" + str(thread_ID) + "  獲取Ev2_Voucher_List開始\n"
    )
    with open(file_path, "a") as file:
        file.write(text_content)

    data = json.dumps(
        {
            "clientType": 0,
            "category": "",
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
    newUrl = voucehrurl + "/voucher/listProducts"
    r = requests.post(newUrl, data=postJson)

    # 解码Base64编码的数据
    cipheredData = b64decode(r.text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # 解密并解除填充
    decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

    # 将解密后的字节转换为字符串（假设它最初是一个字符串）
    originalData = decryptedData.decode("UTF-8")
    # print("voucherData:",originalData)
    json_object = json.loads(originalData)
    products = json_object["data"]["products"]

    # ======================獲取List結束 Content開始==============
    current_time = datetime.now()
    nowFormat2 = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
    text_content = (
        str([nowFormat2]) + "執行續" + str(thread_ID) + "  獲取Ev2_Voucher_List結束\n"
    )

    with open(file_path, "a") as file:
        file.write(text_content)
        file.write(
            str([nowFormat2]) + "執行續" + str(thread_ID) + "  獲取所有Ev2_Voucher_Content開始\n"
        )
        # ======================獲取List結束 Content開始==============

    with open(file_path, "a") as file:
        file.write(text_content)
    for item in products:
        data = json.dumps(
            {
                "clientType": 0,
                "category": item["category"],
                "itemCode": item["itemCode"],
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
        newUrl = voucehrurl + "/voucher/productDetail"
        r = requests.post(newUrl, data=postJson)

        # 解码Base64编码的数据
        cipheredData = b64decode(r.text)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # 解密并解除填充
        decryptedData = unpad(cipher.decrypt(cipheredData), AES.block_size)

        # 将解密后的字节转换为字符串（假设它最初是一个字符串）
        originalData = decryptedData.decode("UTF-8")

    # ======================獲取Conten結束 Content開始到結束時間差==============
    current_time = datetime.now()
    nowFormat3 = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
    text_content = (
        str([nowFormat3]) + "執行續" + str(thread_ID) + "  獲取所有Ev2_Voucher_Content結束\n"
    )

    time1 = datetime.strptime(nowFormat2, "%Y-%m-%d %H-%M-%S-%f")
    time2 = datetime.strptime(nowFormat3, "%Y-%m-%d %H-%M-%S-%f")
    time_difference = time2 - time1
    with open(file_path, "a") as file:
        file.write(text_content)
        file.write(
            str([nowFormat3])
            + "執行續"
            + str(thread_ID)
            + "獲取所有Ev2_Voucher_Content結束-"
            + "時間相差:"
            + str(time_difference.total_seconds())
            + "\n"
        )
    # ======================獲取Conten結束 Content開始到結束時間差==============

    current_time = datetime.now()
    nowFormat4 = current_time.strftime("%Y-%m-%d %H-%M-%S-%f")[:-3]
    time1 = datetime.strptime(nowFormat1, "%Y-%m-%d %H-%M-%S-%f")
    time2 = datetime.strptime(nowFormat4, "%Y-%m-%d %H-%M-%S-%f")

    # 计算时间差
    time_difference = time2 - time1

    with open(file_path, "a") as file:
        file.write(
            str([nowFormat2])
            + "執行續"
            + str(thread_ID)
            + "獲取Ev2_Voucher結束-"
            + "時間相差:"
            + str(time_difference.total_seconds())
            + "\n"
        )
        # file.write("----------------------------------------------------------\n")


CreateFile()
deviceRegAndLogin1()
# deviceRegAndLogin2()

lock = threading.Lock()

running = True


def getMainPgaeThread1(thread_ID):
    global running
    while running:
        getMainPgae(thread_ID)


def getMainPgaeThread2(thread_ID):
    global running
    while running:
        getMainPgae2(thread_ID)


def getVoucherThread(thread_ID):
    global running
    while running:
        getVoucher(thread_ID)


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
print(thread_count)
# 创建并启动线程
threads = []
for i in range(1, thread_count + 1):
    thread1 = threading.Thread(target=getMainPgaeThread1, args=(i,))
    # thread2 = threading.Thread(target=getMainPgaeThread2, args=(i,))
    threads.append(thread1)
    # threads.append(thread2)
    thread1.start()
    # thread2.start()
    # thread_voucher = threading.Thread(target=getVoucherThread, args=(i,))
    # threads.append(thread_voucher)
    # thread_voucher.start()

# 等待所有线程完成
for thread in threads:
    thread.join()

# 主线程等待用户输入以停止线程
# input("按Enter键停止執行續...")
running = False  # 设置标志以停止线程
for thread in threads:
    thread.join()

print("執行續已停止")
