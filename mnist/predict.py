import tensorflow as tf 
import tensorflow_datasets as tfds 
import numpy as np
import logging 
import os

def make_predict(input_img: np.ndarray):
    logger = logging.getLogger(__name__)
    trained_model = tf.keras.models.load_model(f'{os.getcwd()}'+'/mnist/saved_model')
    trained_model.summary(print_fn=logger.info)

    predict = trained_model.predict(input_img)

    return np.argmax(predict)
