import requests,json
from bs4 import BeautifulSoup

from flask import Flask, render_template, request, make_response, jsonify

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
app = Flask(__name__)


@app.route("/")
def index():
    homepage = "<h1>黃汶樺Python網頁</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=黃汶樺>傳送使用者暱稱</a><br>"
    homepage += "<a href=/account>網頁表單輸入實例</a><br>"
    homepage += "<a href=/I>黃汶樺簡介網頁</a><br>"
    homepage += "<a href=/search>食物查詢</a><br>"
    homepage += "<a href=/webhook>查詢</a><br>"
    return homepage


@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html", datetime = str(now))

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    user = request.values.get("nick")
    return render_template("welcome.html", name=user)

@app.route("/I")
def aboutme():
    user = request.values.get("nick")
    return render_template("aboutme.html")

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        Cond = request.form["keyword"]
        Time = request.form["Time"]
        result = "您輸入的地點關鍵字是：" + Cond
        result = "您輸入的時段關鍵字是：" + Time

        db = firestore.client()
        collection_ref = db.collection("食物")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if Cond in dict["地點"] and Time in dict["時段"]:
                result += "地點:"+dict["地點"]+"\t"+"\t"+"時段:"+dict["時段"]+"\t"+"\t"+"店家名稱:"+dict["店家名稱"] +"\t"+"\t"+ "地址:" + dict["地址"] +"\t"+"\t"+ "營業時間:"
                result += dict["營業時間"] +"\t"+"\t"+ "評價:" + dict["評價"] +"\t"+"\t"+ "類型:"+ dict["類型"]+"<br>"+"<br>"
        
        if result =="":
            result = "抱歉,查無相關條件的資訊"
        
        return result
    else:
        return render_template("search.html")

@app.route("/webhook", methods=["POST"])
def webhook():
# build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    #msg =  req.get("queryResult").get("queryText")
    #info = "動作：" + action + "； 查詢內容：" + msg
    if (action == "food"):
        location =  req.get("queryResult").get("parameters").get("location")
        time =  req.get("queryResult").get("parameters").get("time")
        info = "您要查詢的地點是" + location + "且您要查詢的時段是" + time+"\n\n\n"
        collection_ref = db.collection("食物")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if location in doc.to_dict()["地點"] and time in doc.to_dict()["時段"]:
                    info += "地點：" + dict["地點"] + "\n\n" 
                    info += "時段：" + dict["時段"] + "\n\n" 
                    info += "店家名稱：" + dict["店家名稱"] + "\n\n" 
                    info += "地址：" + dict["地址"] + "\n\n"
                    info += "營業時間：" + dict["營業時間"] + "\n\n"
                    info += "評價：" + dict["評價"] + "\n\n" 
                    info += "類型：" + dict["類型"] + "\n"      
        if not found::
            info += "抱歉，目前無符合這個關鍵字的相關資訊喔" 
        
        return info
        #info += result
    return make_response(jsonify({"fulfillmentText": info}))

if __name__ == "__main__":
    app.run()
