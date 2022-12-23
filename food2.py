import requests,json
from bs4 import BeautifulSoup

from flask import Flask, render_template, request, abort,make_response,jsonify
from datetime import datetime, timezone, timedelta

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


app = Flask(__name__)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        Cond = request.form["keyword"]
        time = request.form["Time"]
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
    action =  req.get("queryResult").get("food")
    # msg =  req.get("queryResult").get("queryText")
    # info = "動作：" + action + "； 查詢內容：" + msg
    if (action == "food"):
        Cond =  req.get("queryResult").get("parameters").get("location")
        keyword =  req.get("queryResult").get("parameters").get("time")
        info = "您要查詢地點的" + Cond + "，關鍵字是：" + keyword + "\n\n"
    #     #if (Cond == "food"):
    #         collection_ref = db.collection("食物")
    #         docs = collection_ref.get()
    #         found = False
    #         for doc in docs:
    #             if keyword in doc.to_dict()["food"]:
    #                 found = True 
    #                 info += "地點：" + doc.to_dict()["地點"] + "\n\n" 
    #                 info += "時段：" + doc.to_dict()["時段"] + "\n\n" 
    #                 info += "店家名稱：" + doc.to_dict()["店家名稱"] + "\n\n" 
    #                 info += "地址：" + doc.to_dict()["地址"] + "\n\n"
    #                 info += "營業時間：" + doc.to_dict()["營業時間"] + "\n\n"
    #                 info += "評價：" + doc.to_dict()["評價"] + "\n\n" 
    #                 info += "類型：" + doc.to_dict()["類型"] + "\n"
    #         if not found:
    #             info += "很抱歉，目前無符合這個關鍵字的相關食物喔"  
    # return make_response(jsonify({"fulfillmentText": info}))


if __name__ == "__main__":
    app.run()