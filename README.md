# A.I vs COVID19
### Using Artificial Intelligence to detect COVID-19 in chest x-rays while comparing accuracy using different loss functions and optimizers

Course: CMPT340 - G. Hamarneh
People: Chester Cervantes <ccervant@sfu.ca>, Nathan Cheung <nca45@sfu.ca>, Linden Kwok
<lindenk@sfu.ca>, Melissa Lee <msl25@sfu.ca>, Evan Yao <evany@sfu.ca>

## What you'll need before downloading
 - Python3 (3.5-3.7)
 - pip (newest version)
 - A ssh key to your sfu gitlab ["But I never used gitlab before"](https://coursys.sfu.ca/2019su-cmpt-470-d1/pages/GitLab)

## Local Installation

This is how to locally install and run the web app via command line:

```shell
# 1. configure your git for gitlab permissions
$ git config --global user.name "*sfu username*"
$ git config --global user.email "*sfu username*@sfu.ca"

# 2. Clone
$ git clone git@csil-git1.cs.surrey.sfu.ca:cmpt-340-fighting-dreamers/ml-vs-covid-webapp.git
$ cd ml-vs-covid-webapp

# 3. Install Python packages
$ pip install -r requirements.txt

# 4. Run web app
$ python main.py

```

Check it out: [http://localhost:5000](http://localhost:5000)


## Model Training

Instructions to train a new model

```shell
# 1. (optional) Download Kaggle Dataset from https://www.kaggle.com/praveengovi/coronahack-chest-xraydataset#IM-0001-0001.jpeg 
    
# 2. (optional) Unzip the dataset into ./dataset
    
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