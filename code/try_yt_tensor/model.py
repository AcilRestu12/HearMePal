import tensorflow as tf
# from tensorflow.keras import layers, models
from keras import layers, models
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout

def create_model(input_size, hidden_size, output_size):
    model = models.Sequential()
    model.add(layers.Input(shape=(input_size,)))
    model.add(layers.Dense(64))
    model.add(layers.Dense(32))
    model.add(layers.Dense(16))
    model.add(layers.Dense(hidden_size))
    model.add(layers.Dense(output_size, activation='softmax'))
    return model

