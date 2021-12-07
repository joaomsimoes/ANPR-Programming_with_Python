import cv2
from keras.models import load_model
import numpy as np

# Load the keras model for classification
# trained using google teachablemachine
# https://teachablemachine.withgoogle.com/train
model = load_model('kerasmodel/keras_model.h5', compile=True)


def model_keras(frame=None):
    # resize the frame to 224x224
    inp = cv2.resize(frame, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)

    # convert to numpy array
    np_image_data = np.asarray(inp)

    # adjust the dimensions of the array for keras
    np_final = np.expand_dims(np_image_data, axis=0)

    # prediciton
    return model.predict(np_final)[0][0]

