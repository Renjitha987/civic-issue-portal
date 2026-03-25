import urllib.request
import json
import uuid

try:
    req = urllib.request.Request('http://127.0.0.1:8000/api/users/login/', data=json.dumps({'username':'citizen1', 'password':'Citizen@123'}).encode(), headers={'Content-Type':'application/json'})
    res = urllib.request.urlopen(req)
    token = json.loads(res.read())['access']

    boundary = uuid.uuid4().hex
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="issue_category"\r\n\r\nWaste\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="location"\r\n\r\nTest Loc\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="description"\r\n\r\nThis is a minimal description.\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="image"; filename="pixel.png"\r\n'
        f'Content-Type: image/png\r\n\r\n'
    ).encode() + b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\xff\xff\xff\x7f\x00\t\xfb\x03\xfd\x12\x1a\x17\xd2\x00\x00\x00\x00IEND\xaeB`\x82' + f'\r\n--{boundary}--\r\n'.encode()

    post_req = urllib.request.Request(
        'http://127.0.0.1:8000/api/complaints/', 
        data=body, 
        headers={'Content-Type':f'multipart/form-data; boundary={boundary}', 'Authorization': f'Bearer {token}'}
    )
    urllib.request.urlopen(post_req)
    print("Success with Image!")
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print(e.read().decode())
except Exception as e:
    print("Other Error:", e)
