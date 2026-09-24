import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model(
    'accident_model/accident_model.keras'
)

def predict_accident(img_path):

    img = tf.keras.preprocessing.image.load_img(
        img_path,
        target_size=(224,224)
    )

    img_array = tf.keras.preprocessing.image.img_to_array(img)

    img_array = img_array / 255.0

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    prediction = model.predict(img_array)

    confidence = float(prediction[0][0])

    if confidence > 0.5:
        return "Non Accident", confidence*100
    else:
        return "Accident", (1-confidence)*100