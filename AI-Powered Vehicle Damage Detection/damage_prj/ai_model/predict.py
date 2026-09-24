import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, 'vehicle_damage_model.h5')

model = tf.keras.models.load_model(model_path)

def predict_image(img_path):

    img = image.load_img(img_path, target_size=(128,128))

    img_array = image.img_to_array(img)

    img_array = img_array / 255.0

    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)[0][0]

    if prediction > 0.5:
        return "Whole", float(prediction)
    else:
        return "Damage", float(1 - prediction)