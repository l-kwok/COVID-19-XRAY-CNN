# Detecting COVID-19 Infected Chest X-RAYS
### Using Artificial Intelligence (Convolutional Neural Network) to detect COVID-19 in chest x-rays 

Developed By: Chester Cervantes <ccervant@sfu.ca>, Nathan Cheung <nca45@sfu.ca>, Linden Kwok
<lindenk@sfu.ca>, Melissa Lee <msl25@sfu.ca>, Evan Yao <evany@sfu.ca>

## What you'll need before downloading
 - Python3 (3.5-3.7)
 - pip (newest version)

## Local Installation
NOTE: A model must be trained before starting the webapp
This is how to locally install and run the web app via command line:

```shell
# 1. Install Python packages
$ pip install -r requirements.txt

# 2. Run web app
$ python main.py

```

Check it out: [http://localhost:5000](http://localhost:5000)


## Model Training

Instructions to train a new model
WARNING: Dataset and Model will be large: Allocate ~1.5GB of space
```shell
# 1. Download Kaggle Dataset from https://www.kaggle.com/praveengovi/coronahack-chest-xraydataset#IM-0001-0001.jpeg 
    
# 2. Unzip the dataset into ./dataset
    
# 3. Load The Datasets 
$ python load.py

# 4. Train the model
$ python train.py

```

## Understanding the code structure and key files

The CNN model was built in Python using open source Keras library and Tensorflow. Keras is designed to run on top of Tensorflow while enabling fast prototyping and supports both convolution neural networks and recurrent networks. The web app was built using Flask framework.

* **main.py**: python backend that recieves image from front end, processes the image, loads a model, gets model predictions, and sends predictions to frontend.
* **model**: contains code to load, train, and declare the CNN classifier model. This repo also contains *trained_model* which is a CNN model that has already been trained with the Kraggle dataset above.
* **templates**: html front end pages. **home.html** is the first page user is redirected to.
* **static**: contains css and javascript for the frontend. **main.js** takes images the user uploads into the html, Post's them to the backend, then listens for prediction results.
