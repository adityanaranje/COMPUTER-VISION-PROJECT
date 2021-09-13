from flask import Flask, render_template, Response, request
from FaceDetect import imagefaces, videofaces
from ObjDetect import videoobjects, imageobjects
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

app = Flask(__name__)

# Creates Connection with the database.
cloud_config = {
    'secure_connect_bundle': 'secure-connect-storesalespredictor.zip'
}
auth_provider = PlainTextAuthProvider('zOZtyozAakSXvUxsyxLoktUw',
                                      'AhSpbJ,f_84-vay_buAntESDL_iyDB+-wUjduUX8,a3P4n8qDOU7WWWPkDH5cOSFJs.x+A-zDYur9cjFHHzdwLDtz97zTmQ+bv0vSfcPeKZaOGLk_jrw6NsAZc+,C55s')
cluster = Cluster(protocol_version=3, cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

session.execute("USE ds")
row = session.execute("select release_version from system.local").one()
if row:
    print(row[0])
else:
    print("An error occurred.")


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

        column = "ID, First_Name, Last_Name, Liked, Feedback"
        value = "{0},'{1}','{2}','{3}','{4}'".format(
            'uuid()', first_name.upper(), last_name.upper(), liked, feedback)

        insert = "INSERT INTO DS.Feedback ({}) VALUES ({});".format(column, value)
        session.execute("USE ds")
        session.execute(insert)
    return render_template('home.html')

# Face Detection
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
