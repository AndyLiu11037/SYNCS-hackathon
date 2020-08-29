from backend import backend
import cv2
import base64
from PIL import Image
import io
import numpy as np
def detect(request):
    feature = 'circles'
    request_json = request.get_json()
    print(request_json)
    try:
        img = base64.b64decode(request_json['image'])
        shape = request.json['shape']
    except:
        return f'jong World!'

    pilImage = Image.open(io.BytesIO(img))
    npImage = np.array(pilImage)
    img = Image.fromarray(npImage)
    score, image = backend(npImage, shape)
    encoded_image = base64.b64encode(image.read())

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Hello World!'
