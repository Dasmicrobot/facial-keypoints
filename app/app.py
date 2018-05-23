import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify

"""
Some helping material:
http://flask.pocoo.org/docs/0.12/
https://github.com/moinudeen/digit-recognizer-flask-cnn
https://github.com/llSourcell/how_to_deploy_a_keras_model_to_production
https://github.com/ssola/python-flask-microservice
https://github.com/leotok/pokedex-as-it-should-be
https://www.pyimagesearch.com/2018/02/05/deep-learning-production-keras-redis-flask-apache/
https://blog.hyperiondev.com/index.php/2018/02/01/deploy-machine-learning-models-flask-api/
"""

app = Flask(__name__)
# limit max file size
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
allowed_extensions = {'png', 'jpg', 'jpeg'}
allowed_content_types = {'image/png', 'image/jpg', 'image/jpeg'}


def allowed_file(file):
    content_type = file.content_type
    if content_type is not None:
        return content_type in allowed_content_types
    filename = file.filename
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/index')
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return "No image part", 400
    file = request.files['image']

    if file.filename == '':
        return "No selected image", 400

    if not allowed_file(file):
        return 'Only {} types are allowed'.format(allowed_extensions), 400

    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier('../detector_architectures/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('../detector_architectures/haarcascade_eye.xml')

    # Detect the faces in image
    resp = dict()
    faces_list = list()
    faces = face_cascade.detectMultiScale(gray, 1.5, 3, minSize=(50, 50))
    for (x, y, w, h) in faces:
        faces_list.append({'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)})
    resp['faces'] = faces_list

    eyes_list = list()
    eyes = eye_cascade.detectMultiScale(gray, 1.1, 2)
    for (x, y, w, h) in eyes:
        eyes_list.append({'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)})
    resp['eyes'] = eyes_list

    return jsonify(data=resp)


if __name__ == "__main__":
    print("Debugging application")
    app.run(host='0.0.0.0', port=8080, debug=True)
