import cv2
import numpy as np
from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR, 'dataset')

recognizer = cv2.face.LBPHFaceRecognizer_create()

detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)


def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    faceSamples = []
    ids = []

    for imagePath in imagePaths:
        try:
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')

            # Improve contrast
            img_numpy = cv2.equalizeHist(img_numpy)

            id = int(os.path.split(imagePath)[-1].split(".")[1])

            faces = detector.detectMultiScale(
                img_numpy,
                scaleFactor=1.05,
                minNeighbors=7
            )

            for (x, y, w, h) in faces:
                if w < 50 or h < 50:
                    continue

                faceSamples.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)

        except:
            continue

    return faceSamples, ids


print("\n[INFO] Training faces...")

faces, ids = getImagesAndLabels(path)

recognizer.train(faces, np.array(ids))

# recognizer.write('trainer/trainer.yml')
# Save trained model
trainer_path = os.path.join(BASE_DIR, 'trainer')

if not os.path.exists(trainer_path):
    os.makedirs(trainer_path)

recognizer.write(os.path.join(trainer_path, 'trainer.yml'))

print(f"\n[INFO] {len(np.unique(ids))} faces trained successfully")