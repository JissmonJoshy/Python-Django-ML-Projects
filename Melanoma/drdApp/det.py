import sys
import os
import glob
import re
from pathlib import Path
from io import BytesIO
import base64
import requests

# Import fast.ai Library
from fastai import *
from fastai.vision import *


from PIL import Image as PILImage


NAME_OF_FILE = 'model_best' # Name of your exported file
PATH_TO_MODELS_DIR = Path(__file__).resolve().parent # by default just use /models in root dir
classes = ['Actinic keratoses', 'Basal cell carcinoma', 'Benign keratosis',
           'Dermatofibroma', 'Melanocytic nevi', 'Melanoma', 'Vascular lesions']

def setup_model_pth(path_to_pth_file, learner_name_to_load, classes):
    data = ImageDataBunch.single_from_classes(
        path_to_pth_file, classes, ds_tfms=get_transforms(), size=224).normalize(imagenet_stats)
    learn = cnn_learner(data, models.densenet169, model_dir='models')
    learn.load(learner_name_to_load, device=torch.device('cpu'))
    return learn

learn = setup_model_pth(PATH_TO_MODELS_DIR, NAME_OF_FILE, classes)

def encode(img):
    img = (image2np(img.data) * 255).astype('uint8')
    pil_img = PILImage.fromarray(img)
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    return base64.b64encode(buff.getvalue()).decode("utf-8")
	
def model_predict(img):
    img = open_image(BytesIO(img))
    pred_class,pred_idx,outputs = learn.predict(img)
    formatted_outputs = ["{:.1f}%".format(value) for value in [x * 100 for x in torch.nn.functional.softmax(outputs, dim=0)]]
    pred_probs = sorted(
            zip(learn.data.classes, map(str, formatted_outputs)),
            key=lambda p: p[1],
            reverse=True
        )
	
    img_data = encode(img)
    print("=======================================================================================")
    print(pred_class)
    print(pred_idx)
    print("=======================================================================================")

    result = {"probs":pred_probs}
    # print(result['probs'])
    # for r in result['probs']:
    #     print(r)
    return result, pred_class
def main(img):
    # img = "./123.jpg"
    inputimg = PILImage.open(img)
    byte_arr = io.BytesIO()
    inputimg.save(byte_arr, format='JPEG')
    image_data = byte_arr.getvalue()
    preds, pred_class = model_predict(image_data)
    return preds, pred_class