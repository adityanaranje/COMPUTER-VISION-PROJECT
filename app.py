from flask import Flask, render_template, Response, request
from FaceDetect import webcameraface, imagefaces, videofaces
from ObjDetect import webcameraobject, videoobjects, imageobjects
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def home():
    if request.method == "POST":
        userFeedback = request.form
        first_name = userFeedback['first name']
        last_name = userFeedback['last name']
        liked = userFeedback['liked']
        feedback = userFeedback['feedback']
        if liked == "1":
            liked = "Yes"
        else:
            liked = "No"

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Feedbackform(First_Name,Last_name,Liked,Feedback) VALUES(%s,%s,%s,%s)",
                    (first_name, last_name, liked, feedback))
        mysql.connection.commit()
        cur.close()
    return render_template('home.html')

# Face Detection

# Webcam


def gen_webcam1(FaceDetect):
    while True:
        frame = FaceDetect.get_frame1()
        yield(b'--frame\r\n'
              b'Content-Type:  image/jpeg\r\n\r\n' + frame +
              b'\r\n\r\n')


@app.route('/webcamface/')
def webcamface():
    return render_template("webcamface.html")


@app.route('/getwebcamface')
def getwebcamface():
    return Response(gen_webcam1(webcameraface()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Video


def gen_video1(FaceDetect):
    while True:
        frame = FaceDetect.get_video1()
        yield(b'--frame\r\n'
              b'Content-Type:  image/jpeg\r\n\r\n' + frame +
              b'\r\n\r\n')


@app.route('/videoface', methods=['GET', 'POST'])
def videoface():
    if request.method == "POST":
        vid = request.files['video1']
        vid.save('uploads/video1.mp4')
    return render_template('videoface.html')


@app.route('/getvideoface')
def getvideoface():
    return Response(gen_video1(videofaces()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Image


def gen_image1(FaceDetect):
    frame = FaceDetect.get_image1()
    yield(b'--frame\r\n'
          b'Content-Type:  image/jpeg\r\n\r\n' + frame +
          b'\r\n\r\n')


@app.route('/imageface', methods=['GET', 'POST'])
def imageface():
    if request.method == "POST":
        img = request.files['image1']
        img.save('uploads/img1.jpg')
    return render_template("imageface.html")


@app.route('/getimageface')
def getimageface():
    return Response(gen_image1(imagefaces()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# Object Detection
# Webcam
def gen_webcam2(ObjDetect):
    while True:
        frame = ObjDetect.get_frame2()
        yield(b'--frame\r\n'
              b'Content-Type:  image/jpeg\r\n\r\n' + frame +
              b'\r\n\r\n')


@app.route('/webcamobject/')
def webcamobject():
    return render_template("webcamobject.html")


@app.route('/getwebcamobject')
def getwebcamobject():
    return Response(gen_webcam2(webcameraobject()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Video


def gen_video2(ObjDetect):
    while True:
        frame = ObjDetect.get_video2()
        yield(b'--frame\r\n'
              b'Content-Type:  image/jpeg\r\n\r\n' + frame +
              b'\r\n\r\n')


@app.route('/videoobject', methods=['GET', 'POST'])
def videoobject():
    if request.method == "POST":
        vid = request.files['video2']
        vid.save('uploads/video2.mp4')
    return render_template("videoobject.html")


@app.route('/getvideoobject')
def getvideoobject():
    return Response(gen_video2(videoobjects()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Image


def gen_image2(ObjDetect):
    while True:
        frame = ObjDetect.get_image2()
        yield(b'--frame\r\n'
              b'Content-Type:  image/jpeg\r\n\r\n' + frame +
              b'\r\n\r\n')


@app.route('/imageobject', methods=['GET', 'POST'])
def imageobject():
    if request.method == "POST":
        img = request.files['image2']
        img.save('uploads/image2.jpg')
    return render_template("imageobject.html")


@app.route('/getimageobject')
def getimageobject():
    return Response(gen_image2(imageobjects()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
