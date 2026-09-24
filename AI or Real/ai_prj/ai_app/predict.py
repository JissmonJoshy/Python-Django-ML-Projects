import tensorflow as tf
import numpy as np

from tensorflow.keras.preprocessing import image

model=tf.keras.models.load_model("ml_model/deepfake_model.keras")

class_names=np.load(
    "ml_model/class_names.npy",
    allow_pickle=True
).item()

labels={v:k for k,v in class_names.items()}

def predict_image(img_path):

    img=image.load_img(img_path,target_size=(224,224))

    img=image.img_to_array(img)

    img=img/255.0

    img=np.expand_dims(img,axis=0)

    prediction=model.predict(img)[0][0]

    confidence=float(prediction)

    if prediction>0.5:
        label=labels[1]
    else:
        label=labels[0]

    return label,confidence