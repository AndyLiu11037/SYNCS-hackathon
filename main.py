from backend import jong
import cv2
import base64
def detect(request):
    feature = 'circles'
    request_json = request.get_json()
    img = base64.b64decode(request_json['image'])
    shape = request.json['shape']

    img = cv2.imread(img, 0)
    score, image = jong(img, feature)
    encoded_image = base64.b64encode(image.tobytes())

    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Hello World!'
