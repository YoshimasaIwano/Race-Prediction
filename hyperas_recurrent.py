import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd

import os
from os import path
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

from tensorflow.python import keras
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Dropout
from tensorflow.python.keras.utils import np_utils
from tensorflow.python.keras import regularizers

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from hyperopt import Trials, STATUS_OK, tpe, rand
from hyperas import optim
from hyperas.distributions import choice, uniform

OWN_FILE_NAME = path.splitext(path.basename('\\Users\\vmlab\\win5.ext'))[0]
def hyperas_model(X_train, Y_train, X_test, Y_test):
    # make model

    model = Sequential()
    model.add(Dense({{choice([256,512,1028])}}, kernel_regularizer = regularizers.l2(0.001), activation = 'relu', input_dim = X_train.shape[1]))
    model.add(Dense({{choice([256,512,1028])}}, kernel_regularizer = regularizers.l2(0.001), activation = 'relu'))
    model.add(Dense({{choice([256,512,1028])}}, kernel_regularizer = regularizers.l2(0.001), activation = 'relu'))
    model.add(Dense(1, activation = 'softmax'))      # output is a number of one

    model.compile(loss = 'mse', metrics = ['mse'])

    history = model.fit(X_train, Y_train, batch_size = {{choice([64,128,256])}}, epochs = 20, validation_split = 0.2)
    
    val_loss, val_acc = model.evaluate(X_test, Y_test, verbose=0)
    print('Best validation acc of epoch:',val_acc)
    print('Best validation loss of epoch:',val_loss)
    return {'loss': -val_acc, 'status':STATUS_OK, 'model':model}

def data():
    X_train = pd.read_csv("csv/data/X_train.csv", sep = ",")
    Y_train = pd.read_csv("csv/data/Y_train.csv", sep = ",")
    X_test = pd.read_csv("csv/data/X_test.csv", sep = ",")
    Y_test = pd.read_csv("csv/data/Y_test.csv", sep = ",")
    return X_train, Y_train, X_test, Y_test

def hyperas_recurrent():
    best_run, best_model = optim.minimize(model = hyperas_model,
                                         data = data,
                                         algo = tpe.suggest,
                                         max_evals = 10,
                                         trials = Trials())
    
    X_test = pd.read_csv("csv/data/X_test.csv", sep = ",")
    Y_test = pd.read_csv("csv/data/Y_test.csv", sep = ",")
    print("Best hyperas:",best_run)
    print("Best model:",best_model.evaluate(X_test,Y_test))
    best_model.save("model/ensamble/{}_simple_model.h5".format(OWN_FILE_NAME))

