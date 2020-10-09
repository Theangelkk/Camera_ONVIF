import cv2
import zmq
import base64
import numpy as np
import simplejson as json

context = zmq.Context()

addr = '127.0.0.1'  # remote ip or localhost
req_port = "10000"  # same as in the pupil remote gui
req = context.socket(zmq.SUB)
req.connect("tcp://{}:{}".format(addr, req_port))

req.setsockopt_string(zmq.SUBSCRIBE, '')

while True:
    try:
        #item = req.recv_string()
        msg = req.recv()

        json_item = json.loads(msg, encoding='utf-8')

        #print("Time = " + str(json_item['Time']))
        #print("ID = " + str(json_item['ID']))

        img = base64.b64decode(json_item['Image'])

        npimg = np.frombuffer(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        cv2.imshow("Stream", source)
        cv2.waitKey(1)

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break