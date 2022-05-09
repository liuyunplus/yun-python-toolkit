import requests
import json


msg = ""
params = {
	"reqType": 0,
    "perception": {
        "inputText": {
            "text": msg
        }
    },
    "userInfo": {
        "apiKey": "ebaefc6cfa3a4d5cb38e3442bed15900",
        "userId": "444056"
    }
}
rep = requests.post("http://openapi.turingapi.com/openapi/api/v2", json=params)
data = json.loads(rep.text)
obj = data["results"][0]
text = obj["values"]["text"]