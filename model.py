import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error

from keras import models
from keras.models import Sequential
from keras.layers import Dense, Input
# from scikeras.wrappers import KerasRegressor
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D



def baseline_model():
    # create model
    model = Sequential()
    model.add(Input(shape=(2,)))
    model.add(Dense(16, activation="relu"))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(1, activation = "relu"))
    # Compile model
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model
    # baseline_model().summary()
model = baseline_model()

def pred(temp,humid):
    dataframe = pd.read_csv("data.csv")
    dataset = dataframe.values
    dataframe.head()
    X = dataframe[['Temperature','Humidity']]
    y = dataframe['WaterFlow']
    x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=42, shuffle=True, test_size=0.3)

    model = baseline_model()
    model.fit(x_train, y_train, epochs = 100, validation_data = (X,y))

    print(model.predict(
        np.array([[temp,humid]]),
        batch_size=None,
        verbose='auto',
        steps=None,
        callbacks=None,
        max_queue_size=10,
        workers=1,
        use_multiprocessing=False
    ))
def main():
    pred(20,70)

if __name__=='__main__':
    main()

