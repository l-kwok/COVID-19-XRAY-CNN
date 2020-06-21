#Imports
import os
import sys

from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect

import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras import models
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from tensorflow.keras.preprocessing import image

import numpy as np

#Image conversion
import base64
import re
import cv2
from PIL import Image
from io import BytesIO

#Make flask module
app = Flask(__name__)

#Labels that classify images
labels = ['COVID-19', 'Pneumonia', 'Normal']

#Trained model directory, will cause error if not previously trained
MODEL_DIR = "model/trained_model"

#Dimention to resize images to
dim = 256

#Homepage that grabs images
@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")
    
#Project documentation page
@app.route("/about")
def about():
    return render_template("about.html")

#Instantiate model, make prediction based on image from front-end
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
	#Get trained model
	model = models.load_model(MODEL_DIR)
	model._make_predict_function()

        #Get the image from post request and process it:
	img = convetJson2PIL(request.json) 			  
	img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY); 
	img = cv2.resize(img, (dim,dim));			
	img = img/255.0 #normalize values 0-1
    	img = np.reshape(img, (1,dim, dim,1)) #reshape [batchxwidthxheightxchannels]

	#Get predicted class, label percents
	softmax = model.predict(img)
	resultClass = labels[np.argmax(softmax)]
	predpercents = softmax * 100.0

        # Serialize and Send the result
        return jsonify(resultClass=resultClass, covid = str(predpercents[0][0]), pneumonia = str(predpercents[0][1]), healthy = str(predpercents[0][2]))

    return None

#Converting the json string image to pil
def convetJson2PIL(img_base64):
    image_data = re.sub('^data:image/.+;base64,', '', img_base64)
    pil_image = Image.open(BytesIO(base64.b64decode(image_data)))
    return pil_image
    

if __name__ == "__main__":
    app.run(debug=True)
