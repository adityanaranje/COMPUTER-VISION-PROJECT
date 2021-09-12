import cv2

faceDetect = cv2.CascadeClassifier('data/haarcascade_facedetect.xml')


# Face detection from webcam
class webcameraface(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame1(self):
        ret, frame = self.video.read()
        faces = faceDetect.detectMultiScale(frame, 1.1, 4)
        for x, y, w, h in faces:
            x1, y1 = x+w, y+h
            cv2.rectangle(frame, (x, y), (x+w, y+h), (127, 255, 0), 1)
            cv2.line(frame, (x, y), (x+25, y), (127, 255, 0), 5)  # Top Left
            cv2.line(frame, (x, y), (x, y+25), (127, 255, 0), 5)

            cv2.line(frame, (x, y1), (x+25, y1), (127, 255, 0), 5)  # Bottom Left
            cv2.line(frame, (x, y1), (x, y1-25), (127, 255, 0), 5)

            cv2.line(frame, (x1, y), (x1-25, y), (127, 255, 0), 5)  # Top Right
            cv2.line(frame, (x1, y), (x1, y+25), (127, 255, 0), 5)

            cv2.line(frame, (x1, y1), (x1-25, y1), (127, 255, 0), 5)  # Bottom right
            cv2.line(frame, (x1, y1), (x1, y1-25), (127, 255, 0), 5)

        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()


# Face detection from video
class videofaces(object):
    def __init__(self):
        self.video = cv2.VideoCapture("uploads/video1.mp4")

    def __del__(self):
        self.video.release()

    def get_video1(self):
        ret, frame = self.video.read()
        faces = faceDetect.detectMultiScale(frame, 1.3, 5)
        for x, y, w, h in faces:
            x1, y1 = x+w, y+h
            cv2.rectangle(frame, (x, y), (x+w, y+h), (127, 255, 0), 1)
            cv2.line(frame, (x, y), (x+25, y), (127, 255, 0), 5)  # Top Left
            cv2.line(frame, (x, y), (x, y+25), (127, 255, 0), 5)

            cv2.line(frame, (x, y1), (x+25, y1), (127, 255, 0), 5)  # Bottom Left
            cv2.line(frame, (x, y1), (x, y1-25), (127, 255, 0), 5)

            cv2.line(frame, (x1, y), (x1-25, y), (127, 255, 0), 5)  # Top Right
            cv2.line(frame, (x1, y), (x1, y+25), (127, 255, 0), 5)

            cv2.line(frame, (x1, y1), (x1-25, y1), (127, 255, 0), 5)  # Bottom right
            cv2.line(frame, (x1, y1), (x1, y1-25), (127, 255, 0), 5)

        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()


# Face detection from image
class imagefaces():
    def get_image1(self):
        image = cv2.imread("uploads/img1.jpg")

        faces = faceDetect.detectMultiScale(image, 1.3, 5)
        for x, y, w, h in faces:
            x1, y1 = x+w, y+h
            cv2.rectangle(image, (x, y), (x+w, y+h), (13, 187, 77), 1)
            cv2.line(image, (x, y), (x+20, y), (13, 187, 77), 3)  # Top Left
            cv2.line(image, (x, y), (x, y+20), (13, 187, 77), 3)

            cv2.line(image, (x, y1), (x+20, y1), (13, 187, 77), 3)  # Bottom Left
            cv2.line(image, (x, y1), (x, y1-20), (13, 187, 77), 3)

            cv2.line(image, (x1, y), (x1-20, y), (13, 187, 77), 3)  # Top Right
            cv2.line(image, (x1, y), (x1, y+20), (13, 187, 77), 3)

            cv2.line(image, (x1, y1), (x1-20, y1), (13, 187, 77), 3)  # Bottom right
            cv2.line(image, (x1, y1), (x1, y1-20), (13, 187, 77), 3)

        ret, jpg = cv2.imencode('.jpg', image)
        return jpg.tobytes()
