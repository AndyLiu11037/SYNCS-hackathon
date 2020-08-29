from backend import jong
import cv2
def detect(request):
    feature = 'circles'
    img = cv2.imread('./sample_circles/12.jpg', 0)
    jong(img, feature)
    request_json = request.get_json()
    print(request_json)
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Hello World!'
