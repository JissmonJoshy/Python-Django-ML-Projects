import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.models import Model
import numpy as np

IMAGE_SIZE=(224,224)
BATCH_SIZE=8

train_datagen=ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_generator=train_datagen.flow_from_directory(
    "dataset/Test",
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="training"
)

validation_generator=train_datagen.flow_from_directory(
    "dataset/Test",
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="validation"
)

base_model=MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224,224,3)
)

base_model.trainable=False

x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(128,activation='relu')(x)
output=Dense(1,activation='sigmoid')(x)

model=Model(inputs=base_model.input,outputs=output)

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=10
)

model.save("ml_model/deepfake_model.keras")

np.save(
    "ml_model/class_names.npy",
    train_generator.class_indices
)

print("Training Completed")