
import os
import string
import random
import json
import requests
import numpy as np
import tensorflow as tf

from flask import Flask, request, redirect, url_for, render_template
from flask_bootstrap import Bootstrap




"""
Here, mobilenet model is used to make predictions
"""
def generate_filename():
    return ''.join(random.choices(string.ascii_lowercase, k=20)) + '.jpg'

def get_prediction(image_path):
    image = tf.keras.preprocessing.image.load_img(image_path, target_size=(SIZE, SIZE))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
    image = np.expand_dims(image, axis=0)

    data = json.dumps({'instances': image.tolist() })
    response = requests.post(MODEL_URI, data=data.encode())
    result = json.loads(response.text)
    prediction = result['predictions'][0]
    class_name = CLASSES[int(prediction > 0.5)]
    return class_name
