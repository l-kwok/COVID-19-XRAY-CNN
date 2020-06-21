#@title load data and pre-processing
from tensorflow.python.keras import preprocessing
import numpy as np
import cv2
import os
from imutils import paths
import sys
import tensorflow as tf
from sklearn.model_selection import train_test_split

sys.path.append("content/drive/My Drive")
from model import ClassifierModel

# Load Data and Pre-processing
dataset_path = "../dataset/master-dataset"
if not os.path.exists(dataset_path):
    print("Dataset has not been loaded! Exiting...")
    print("Note: Run `python load.py` first")
    exit()

 
data=[]
labels=[]
imagePaths = list(paths.list_images(dataset_path))

print("Loading Images...")
i=1
dim = 256
for path in imagePaths:
    label = path.split(os.path.sep)[-2]
    labels.append(label)

    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (dim, dim))
    data.append(image)
    if (i%20==0 or i==len(imagePaths)):
      print("Fromatting Progress {}/{}".format(i,len(imagePaths)))
    i = i+1

data = np.array(data)/255.0
labels = np.array(labels)

X = np.reshape(data,(len(data),dim,dim,1))
Y = np.zeros((len(labels),3))
for i in range(len(labels)):
  if (labels[i]=='COVID-19'):
    Y[i] = [1, 0, 0]
  elif (labels[i]=='Normal'):
    Y[i] = [0, 0, 1]
  else:
    Y[i] = [0, 1, 0]
print("Images Loaded and Formatted")

## Split them into Train data and Test data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

## Data generator, used for Data Augmentation
dg = preprocessing.image.ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1)

# tensor board
fp = "/content/drive/My Drive/CMPT340_Project/Log/tmp"
tb = tf.keras.callbacks.TensorBoard(log_dir=fp, histogram_freq=0,  
          write_graph=True, write_images=True)

# Initialize Model
batch_size=250
epochs=50
callbacks=None
validation_data=None

classifierModel = ClassifierModel(num_type=3, dim=dim)
model = classifierModel.get_model()

# # train without data augmentation
# model.fit(X, Y,
#                          batch_size=batch_size,
#                          epochs=epochs,
#                          callbacks=callbacks,
#                          validation_data=validation_data
#                          )

# train with data augmentation
model.fit_generator(dg.flow(X_train, Y_train, 
                                                       batch_size =batch_size),
                                                       steps_per_epoch=len(X) / batch_size, 
                                                       epochs=epochs,
                                                       callbacks=callbacks,
                                                       validation_data=validation_data)

model.save("trained_model")
loss, accuracy = model.evaluate(X_test, Y_test)
print( "Loss is {}".format( loss ) , "Accuracy is {} %".format( accuracy * 100 ) )
