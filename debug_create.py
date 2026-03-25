import urllib.request
import json
import uuid

# Create a dummy image larger than 5MB
# However, to pass PIL validation, we just need a valid image header, but we can't easily spoof a 6MB PNG that passes PIL without creating a huge file.
# Wait, if we create a huge text file but name it .png... PIL will fail and give 400.
# So we must create a valid 6MB image!
from PIL import Image
import io

img = Image.new('RGB', (4000, 4000), color = 'blue')
img_byte_arr = io.BytesIO()
img.save(img_byte_arr, format='PNG')
img_bytes = img_byte_arr.getvalue()

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
        f'Content-Disposition: form-data; name="image"; filename="huge.png"\r\n'
        f'Content-Type: image/png\r\n\r\n'
    ).encode() + img_bytes + f'\r\n--{boundary}--\r\n'.encode()

    post_req = urllib.request.Request(
        'http://127.0.0.1:8000/api/complaints/', 
        data=body, 
        headers={'Content-Type':f'multipart/form-data; boundary={boundary}', 'Authorization': f'Bearer {token}'}
    )
    res = urllib.request.urlopen(post_req)
    print("Success with Huge Image!")
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print(e.read().decode())
except Exception as e:
    print("Other Error:", e)
