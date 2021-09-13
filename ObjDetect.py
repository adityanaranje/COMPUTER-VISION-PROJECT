import cv2
import numpy as np
thres = 0.5  # Threshold to detect object
nms_threshold = 0.2


classNames = []
classFile = "data/coco.names"
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath1 = "data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath1 = "data/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath1, configPath1)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

COLORS = np.random.randint(0, 255, size=(len(classNames), 3), dtype="uint8")

# Object detection from Video


class videoobjects(object):
    def __init__(self):
        self.video = cv2.VideoCapture("uploads/video2.mp4")

    def __del__(self):
        self.video.release()

    def get_video2(self):
        success, img = self.video.read()

        if img.shape[1] > 1500 and img.shape[1] < 2000 or img.shape[0] > 1500 and img.shape[0] < 2000:
            img = cv2.resize(img, (int(img.shape[1]*0.55), int(img.shape[0]*0.55)))
        if img.shape[1] > 2000 and img.shape[1] < 3000 or img.shape[0] > 2000 and img.shape[0] < 3000:
            img = cv2.resize(img, (int(img.shape[1]*0.4), int(img.shape[0]*0.4)))
        if img.shape[1] > 3000 or img.shape[0] > 3000:
            img = cv2.resize(img, (int(img.shape[1]*0.2), int(img.shape[0]*0.2)))

        classIds, confs, bbox = net.detect(img, confThreshold=thres)
        bbox = list(bbox)
        confs = list(np.array(confs).reshape(1, -1)[0])
        confs = list(map(float, confs))
        # print(type(confs[0]))
        # print(confs)

        indices = cv2.dnn.NMSBoxes(bbox, confs, thres, nms_threshold)
        # print(indices)

        for i in indices:
            i = i[0]
            box = bbox[i]
            color = [int(c) for c in COLORS[classIds[i][0]-1]]
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(img, (x, y), (x+w, h+y), color=color, thickness=2)
            cv2.putText(img, classNames[classIds[i][0]-1].upper(), (box[0]+10, box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)

        ret, jpg = cv2.imencode('.jpg', img)
        return jpg.tobytes()


# Object detection from Image


class imageobjects():
    def get_image2(self):
        img = cv2.imread("uploads/image2.jpg")
        classIds, confs, bbox = net.detect(img, confThreshold=thres)
        bbox = list(bbox)
        confs = list(np.array(confs).reshape(1, -1)[0])
        confs = list(map(float, confs))
        # print(type(confs[0]))
        # print(confs)

        indices = cv2.dnn.NMSBoxes(bbox, confs, thres, nms_threshold)
        # print(indices)

        for i in indices:
            i = i[0]
            box = bbox[i]
            color = [int(c) for c in COLORS[classIds[i][0]-1]]
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(img, (x, y), (x+w, h+y), color=color, thickness=2)
            cv2.putText(img, classNames[classIds[i][0]-1].upper(), (box[0]+10, box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)

        ret, jpg = cv2.imencode('.jpg', img)
        return jpg.tobytes()
