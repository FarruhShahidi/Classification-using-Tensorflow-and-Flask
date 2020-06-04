import os
import string
import random
import json
import requests
import numpy as np
import tensorflow as tf

from flask import Flask, request, redirect, url_for, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

"""
Constants
"""
MODEL_URI = 'http://localhost:8502/v1/models/pets:predict'
OUTPUT_DIR = 'static'
CLASSES = ['Cat', 'Dog']
SIZE = 128

# importing predictions

import utils


"""
Routes
"""
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            if uploaded_file.filename[-3:] in ['jpg', 'png']:
                image_path = os.path.join(OUTPUT_DIR, generate_filename())
                uploaded_file.save(image_path)
                class_name = get_prediction(image_path)
                result = {
                    'class_name': class_name,
                    'path_to_image': image_path,
                    'size': SIZE
                }
                return render_template('show.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
