from backend import backend
import cv2
import base64
from PIL import Image
import io
import numpy as np
import json
def detect(request):
    ENCODING = 'utf-8'
    feature = 'circles'
    request_json = request.get_json()
    print(request_json)
    try:
        img = base64.b64decode(request_json['image'])
        shape = request.json['shape']
    except:
        return f'jong World!'

    pilImage = Image.open(io.BytesIO(img))
    my_string = ""
    with open("./sample_circles/comp.jpg", "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
    npImage = np.array(pilImage)
    img = Image.fromarray(npImage)
    score, image = backend(npImage, shape)
    if score == -1000:
        return (200,my_string.decode('utf-8'))
    encoded_image = base64.b64encode(image.getvalue())
    print(encoded_image)
    base64_string = encoded_image.decode(ENCODING)
    status = 200
    print(str(score))
    body = json.dumps({"score": str(score), "image": base64_string})
    return (body,status)
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Hello World!'
