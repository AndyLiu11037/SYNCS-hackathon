from backend import jong
import cv2
import base64
from PIL import Image
from io import StringIO
import numpy as np
import cv2
def detect(request):
    feature = 'circles'
    request_json = request.get_json()
    try:
        img = base64.b64decode(request_json['image'])
        shape = request.json['shape']
    except:
        return f'jong World!'

    pilImage = Image.open(StringIO(img))
    npImage = np.array(pilImage)
    img = cv2.fromarray(npImage)
    score, image = jong(img, shape)
    encoded_image = base64.b64encode(image.tobytes())

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Hello World!'
