import json
import pyodbc
from flask import Flask, current_app, request, Response
from flask_cors import CORS
import base64
import datetime
import os
from PIL import Image
import time

app = Flask(__name__)
CORS(app)

def Select_SQL(sql):
    conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=210.68.227.123,3134; DATABASE=YongKamg; UID=sa; PWD=Acme-70472615')
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
    conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=210.68.227.123,3134; DATABASE=YongKamg; UID=sa; PWD=Acme-70472615')
    cursor = conn.cursor()
    sqlstr = sql
    cursor.execute(sqlstr)
    conn.commit()
    conn.close()
    return "success"

@app.route('/Login',methods=['POST'])
def Login():
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))

    account = json_data.get("account")
    password = json_data.get("password")

    sql = "SELECT competence3 FROM [dbo].[Staff] WHERE status = '在職' AND account='{}' AND password='{}'".format(account,password)
    items = Select_SQL(sql)

    data = {
        'Authority':items,
    }
    return data

@app.route('/Select_task',methods=['POST'])
def Select_task():
    sql_where = ''

    # today = datetime.date.today()
    # Now_hour = datetime.datetime.now().hour
    # if Now_hour >= 9 and Now_hour < 17:
    #     sql_where = str(today)+' 08:00'
    # elif Now_hour >= 17 or Now_hour == 0:
    #     sql_where = str(today)+' 16:00'
    # elif Now_hour >= 1 and Now_hour < 9:
    #     sql_where = str(today)+' 00:00'

    sql = """SELECT a.[id_C], a.[unit] ,a.[location] ,a.[rfid] ,a.[item1] ,a.[reference1] ,a.[item2] ,a.[reference2] ,a.[item3]
    ,a.[reference3],a.[item4],a.[reference4],a.[item5],a.[reference5],a.[create_time],b.name_S,b.number
     FROM [dbo].[Check] a left join Category_Small b on a.id_S = b.id_S 
    """
    items = Select_SQL(sql)

    data = {
        'Task':items,
    }
    return data

@app.route('/NFCID_List',methods=['POST'])
def NFCID_List():
    sql = "SELECT RFID from Category_Small"
    items = Select_SQL(sql)

    data = {
        'data':items,
    }
    return data

@app.route('/Check_Device',methods=['POST'])
def Check_Device():
    sql = "SELECT id_S,number,name_S from Category_Small WHERE RFID IS NULL AND checking = '是'"
    items = Select_SQL(sql)

    data = {
        'device':items,
    }
    return data

@app.route('/Update_RFID',methods=['POST'])
def Update_RFID():
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))

    Result = json_data.get("data")
    print(Result)

    for i in Result:
        if len(i) == 1:
            continue
        else:
            num = i[0]
            RFID = i[1]
            sql = "UPDATE Category_Small SET RFID = '{}' WHERE id_S = '{}'".format(RFID,num)
            Insert_SQL(sql)

    return_data = {'data':'success'}
    return return_data

@app.route('/Search_device',methods=['POST'])
def Search_device():
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))

    Result = json_data.get("data")

    sql = "SELECT id_S,number,RFID,name_S FROM Category_Small WHERE checking = '是' AND number LIKE '{}'".format(Result+'%')
    device = Select_SQL(sql)
    return_data = {'data':device}
    return return_data

@app.route('/Edit_RFID',methods=['POST'])
def Edit_RFID():
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))

    Result = json_data.get("data")
    for i in Result:
        num = i[0]
        device = i[1]
        RFID = i[2]
        sql = "UPDATE Category_Small SET RFID = '{}' WHERE id_S = '{}' AND number='{}'".format(RFID,num,device)
        Insert_SQL(sql)

    return_data = {'data':'success'}
    return return_data

# @app.route('/Upload_image',methods=['POST'])
# def Upload_image():
#     data = request.get_data()
#     json_data = json.loads(data.decode("UTF-8"))
#     img_bs64 = json_data.get("Image")
#     decode_img = base64.b64decode(img_bs64)
#     with open('C:/Derek/image/2.jpeg','wb') as f:
#         f.write(decode_img)
#     data = {
#         'success':'success',
#     }
#     return data

# @app.route('/Check_status',methods=['POST'])
# def Check_status():
#     data = request.get_data()
#     json_data = json.loads(data.decode("UTF-8"))
#     flag = json_data.get("flag")

#     sql = "SELECT a.name_S,a.number,convert(date,c.work_time,108) FROM [dbo].[Category_Small] a left join [Check] b on b.id_S = a.id_S left join [Check_Result] c on b.id_C = c.id_C WHERE b.flag = '{}' AND convert(date,[create_time],23) = convert(date,getdate(),23)".format(flag)
#     device = Select_SQL(sql)
#     return_data = {'data':device}
#     return return_data

@app.route('/Insert_result',methods=['POST'])
def Insert_res():
    NFC_ID = ""
    id_C = ""
    result1 = ""
    result2 = ""
    result3 = ""
    result4 = ""
    result5 = ""

    abnormal1 = ""
    abnormal2 = ""
    abnormal3 = ""
    abnormal4 = ""
    abnormal5 = ""
    data = request.get_data()
    json_data = json.loads(data.decode("UTF-8"))

    Result = json_data.get("finish_task")
    ab_Result = json_data.get("abnormal_task")
    img_Result = json_data.get("ab_img_task")

    for a in img_Result:
        str_To_ary = a.split(',')
        for b in range(len(str_To_ary)):
            if b == 0:
                continue
            decode_img = base64.b64decode(str_To_ary[b])
            today = str(datetime.date.today())

            if not os.path.isdir('D:/Image/'+today+''):
                os.mkdir('D:/Image/'+today+'')
            
            nowhour = time.strftime('%H')
            nowmin = time.strftime('%M')
            hour_min = str(nowhour+nowmin)
            with open('D:/Image/'+today+'/'+str_To_ary[0]+'_'+str(hour_min)+'.jpeg','wb') as f: #檔名 日期編號_b.jpeg
                f.write(decode_img)

                #轉照片
                im = Image.open('D:/Image/'+today+'/'+str_To_ary[0]+'_'+str(hour_min)+'.jpeg')
                im_rotate = im.rotate(-90, expand=1)
                im_rotate.save('D:/Image/'+today+'/'+str_To_ary[0]+'_'+str(hour_min)+'.jpeg')

    for i in Result:
        str_To_ary = i.split(',')
        for x in range(len(str_To_ary)-2): #陣列後面2位是固定的NFC & id_C 單獨拉出來處理
            if len(str_To_ary) == 3:
                NFC_ID = str_To_ary[1]
                id_C = str_To_ary[2]
                sql = "INSERT INTO [dbo].[Check_Result] (id_C,result_rfid,result1,result2,result3,result4,result5,remark) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(id_C,NFC_ID,'','','','','','未巡檢')
                Insert_SQL(sql)

            elif str_To_ary[x] == '0':
                num = x+1
                result1 = str_To_ary[num]

            elif str_To_ary[x] == '1':
                num = x+1
                result2 = str_To_ary[num]

            elif str_To_ary[x] == '2':
                num = x+1
                result3 = str_To_ary[num]

            elif str_To_ary[x] == '3':
                num = x+1
                result4 = str_To_ary[num]

            elif str_To_ary[x] == '4':
                num = x+1
                result5 = str_To_ary[num]

            elif x == len(str_To_ary)-3: #因為x是從0開始 所以要多減一位
                NFC_ID = str_To_ary[len(str_To_ary)-2]
                id_C = str_To_ary[len(str_To_ary)-1]
                sql = "INSERT INTO [dbo].[Check_Result] (id_C,result_rfid,result1,result2,result3,result4,result5,remark) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(id_C,NFC_ID,result1,result2,result3,result4,result5,'正常')
                Insert_SQL(sql)
                sql2 = "UPDATE [dbo].[Check] SET flag = '1' WHERE id_C = '{}'".format(id_C)
                Insert_SQL(sql2) 
                result1 = "" #insert後把變數清掉
                result2 = ""
                result3 = ""
                result4 = ""
                result5 = ""
                
        
    for y in ab_Result:
        str_To_ary = y.split(',')
        for z in range(len(str_To_ary)-2): #陣列後面2位是固定的NFC & id_C 單獨拉出來處理
            if str_To_ary[z] == '0':
                num = z+1
                abnormal1 = str_To_ary[num]

            elif str_To_ary[z] == '1':
                num = z+1
                abnormal2 = str_To_ary[num]

            elif str_To_ary[z] == '2':
                num = z+1
                abnormal3 = str_To_ary[num]

            elif str_To_ary[z] == '3':
                num = z+1
                abnormal4 = str_To_ary[num]

            elif str_To_ary[z] == '4':
                num = z+1
                abnormal5 = str_To_ary[num]

            elif z == len(str_To_ary)-3:
                ab_len = len(str_To_ary)
                NFC_ID = str_To_ary[ab_len-2]
                id_C = str_To_ary[ab_len-1]
                sql = "UPDATE [dbo].[Check_Result] SET abnormal1 = '{}',abnormal2 = '{}',abnormal3 = '{}',abnormal4 = '{}',abnormal5 = '{}',remark='{}' WHERE id_C = '{}' AND result_rfid = '{}'".format(abnormal1,abnormal2,abnormal3,abnormal4,abnormal5,'異常',id_C,NFC_ID)
                Insert_SQL(sql)
                sql2 = "UPDATE [dbo].[Check] SET flag = '1' WHERE id_C = '{}'".format(id_C)
                Insert_SQL(sql2)
                abnormal1 = "" #insert後把變數清掉
                abnormal2 = ""
                abnormal3 = ""
                abnormal4 = ""
                abnormal5 = ""
            
    data = {
        'message':'success',
    }
    return data

if __name__ == "__main__": 
    app.run(host="192.168.2.81", port=5008)