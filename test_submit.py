import urllib.request
import json

try:
    req = urllib.request.Request('http://127.0.0.1:8000/api/users/login/', data=json.dumps({'username':'citizen1', 'password':'Citizen@123'}).encode(), headers={'Content-Type':'application/json'})
    res = urllib.request.urlopen(req)
    token = json.loads(res.read())['access']

    data = b'--boundary\r\nContent-Disposition: form-data; name="issue_category"\r\n\r\nWaste\r\n--boundary\r\nContent-Disposition: form-data; name="location"\r\n\r\nTest Loc\r\n--boundary\r\nContent-Disposition: form-data; name="description"\r\n\r\nThis is a minimal description.\r\n--boundary--\r\n'

    post_req = urllib.request.Request('http://127.0.0.1:8000/api/complaints/', data=data, headers={'Content-Type':'multipart/form-data; boundary=boundary', 'Authorization': f'Bearer {token}'})
    try:
        urllib.request.urlopen(post_req)
        print("Success!")
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code)
        print(e.read().decode())
    except Exception as e:
        print("Other Error:", e)
except Exception as e:
    print("Login Error:", e)
