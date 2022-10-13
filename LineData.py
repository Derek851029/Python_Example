from flask import Flask, current_app, request, Response
from flask_cors import CORS
import pyodbc
import requests
import json

app = Flask(__name__)
CORS(app)

def Line_Post(UserID,text):
    url = 'http://210.68.227.123:7009/PushFaceData.aspx/PushLineMsg'
    # LINE 群發訊息資料 --> text: 要發的訊息內容
    data = {'ID':UserID,'msg':text,'type':'text'}
    headers = {
              'Content-Type': 'application/json'
            }
    r = requests.post(url,headers=headers ,data = json.dumps(data,separators=(',', ':')))
    return 'success'

def Select_SQL(sql):
    conn = pyodbc.connect('DRIVER={SQL Server}; SERVER=210.68.227.123,3134; DATABASE=APEX_Health_Hotel; UID=sa; PWD=Acme-70472615')
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

@app.route('/Line_Data',methods=['POST'])
def Line_Data():
    data = request.get_data()
    data = data.decode('utf-8')
    print(data)
    sql = "select UserID from [dbo].[LineMember]"
    User_ID = Select_SQL(sql)
    for i in User_ID:
        Line_Post(i[0],data)
    return ""
    
if __name__ == "__main__":
    app.run(host='192.168.2.168', port=5010)