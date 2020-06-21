from tensorflow.python.keras import models , optimizers , losses ,activations
from tensorflow.python.keras.layers import *
import tensorflow as tf
import time
import os
import numpy as np

class ClassifierModel(object):

    def __init__( self, num_type, dim, num_dense_tensor=100, dropout_rate=0.5, optimizer=optimizers.Adam(), loss_function=losses.categorical_crossentropy):
        self.__dim = dim
        input_shape = (self.__dim,self.__dim,1)

        self.__NEURAL_NETWORK = [
                                
                Conv2D(32, kernel_size=(3, 3) , strides=1 , activation=activations.relu,input_shape=input_shape),
                MaxPooling2D(pool_size=(2, 2), strides=2),

                Conv2D(64, kernel_size=(3, 3) , strides=1 , activation=activations.relu),
                MaxPooling2D(pool_size=(2, 2) , strides=2),     

                Flatten(),          
                
                Dropout(dropout_rate),

                Dense( num_dense_tensor, activation=activations.relu) ,
                Dense( num_type, activation=tf.nn.softmax)                         
        ]

        self.__model = tf.keras.Sequential(self.__NEURAL_NETWORK)

        self.__model.compile(
                optimizer=optimizer,
                loss= loss_function,
                metrics=[ 'accuracy' ] ,
            )
      
    def get_model(self):
        return self.__model