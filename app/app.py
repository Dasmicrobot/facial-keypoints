import os

import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, make_response, jsonify
from keras.models import model_from_json

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
allowed_extensions = set(['png', 'jpg', 'jpeg'])
allowed_content_types = set(['image/png', 'image/jpg', 'image/jpeg'])


def allowed_file(file):
    content_type = file.content_type
    if content_type is not None:
        return content_type in allowed_content_types
    filename = file.filename
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def convert_image_for_prediction(image_file):
    pass


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

    # Detect the faces in image
    faces_list = list()
    faces = face_cascade.detectMultiScale(gray, 1.5, 3, minSize=(50, 50))
    for (x, y, w, h) in faces:
        faces_list.append({'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)})

    return jsonify(data=faces_list)


def draw_face_boxes(img, faces):
    # Get the bounding box for each detected face
    for (x, y, w, h) in faces:
        # Add a red bounding box to the detections image
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)


def cv2_image_to_response(img):
    _, buff = cv2.imencode(".jpg", img)
    response = make_response(buff.tobytes())
    response.headers['Content-Type'] = 'image/jpeg'
    return response


def load_model():
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    print("Model loaded loaded from json")

    # load woeights into new model
    loaded_model.load_weights("model.h5")
    print("Model weights loaded from disk")

    # compile and evaluate loaded model
    loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    print("Model compiled")

    graph = tf.get_default_graph()
    print("Tensorflow graph obtained")

    return loaded_model, graph


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))

    print("Start application")
    app.run(host='0.0.0.0', port=port, debug=True)
