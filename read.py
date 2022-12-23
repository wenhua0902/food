import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

Cond = input("請輸入您要查詢的地點關鍵字:")
Time = input("請輸入您要查詢的時段關鍵字:")

collection_ref = db.collection("食物")
docs = collection_ref.get()
result = ""
for doc in docs:
	dict = doc.to_dict()
	if Cond in dict["地點"]:
		result += "地點:"+dict["地點"]+"時段:"+dict["時段"]+"店家名稱:"+dict["店家名稱"] + "地址:" + dict["地址"] + "營業時間:"
		result += dict["營業時間"] + "評價:" + dict["評價"] + "類型:"+ dict["類型"]+"\n"

	if Time in dict["時段"]:
		result += "地點:"+dict["地點"]+"時段:"+dict["時段"]+"店家名稱:"+dict["店家名稱"] + "地址:" + dict["地址"] + "營業時間:"
		result += dict["營業時間"] + "評價:" + dict["評價"] + "類型:"+ dict["類型"]+"\n"
print(result)
