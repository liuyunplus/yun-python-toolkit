import json

with open("data.json", 'r') as file:
    jsonData = json.load(file)

base64 = jsonData['data']

html = """
<!doctype html>
<html>
	<head>
		<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
	</head>
	<body>
		<img src="data:image/png;base64,%s"/>
	</body>
</html>
""" % base64

with open("output.html", "w") as f:
    f.write(html)
