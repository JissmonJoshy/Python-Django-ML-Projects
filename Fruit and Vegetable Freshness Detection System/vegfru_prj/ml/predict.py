import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "fruit_model.keras")

LABEL_PATH = os.path.join(BASE_DIR, "labels.txt")

model = tf.keras.models.load_model(MODEL_PATH)

with open(LABEL_PATH) as f:
    labels = [line.strip() for line in f]


def predict_image(image_path):

    img = image.load_img(
        image_path,
        target_size=(224,224)
    )

    img = image.img_to_array(img)

    img = img/255.0

    img = np.expand_dims(img,axis=0)

    prediction = model.predict(img,verbose=0)

    index = np.argmax(prediction)

    class_name = labels[index]

    confidence = float(prediction[0][index])*100

    return class_name,confidence