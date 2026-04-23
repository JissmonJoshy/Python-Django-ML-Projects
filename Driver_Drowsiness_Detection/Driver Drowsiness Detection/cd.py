import cv2
import os
import numpy as np
from tensorflow.keras.models import load_model
from pygame import mixer

# Initialize alarm
mixer.init()
sound = mixer.Sound('alarm.wav')

# Load Haar cascades
face = cv2.CascadeClassifier('haar cascade files/haarcascade_frontalface_alt.xml')
leye = cv2.CascadeClassifier('haar cascade files/haarcascade_lefteye_2splits.xml')
reye = cv2.CascadeClassifier('haar cascade files/haarcascade_righteye_2splits.xml')

# Load model
model = load_model('models/cnncat2.h5')

# Labels
labels = ['Closed', 'Open']

# Start webcam
cap = cv2.VideoCapture(0)

score = 0
thicc = 2
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face.detectMultiScale(gray, 1.1, 5)
    left_eye = leye.detectMultiScale(gray)
    right_eye = reye.detectMultiScale(gray)

    # Default predictions
    rpred = [1]
    lpred = [1]

    # RIGHT EYE
    for (x, y, w, h) in right_eye:
        r_eye = frame[y:y+h, x:x+w]
        r_eye = cv2.cvtColor(r_eye, cv2.COLOR_BGR2GRAY)
        r_eye = cv2.resize(r_eye, (24, 24))
        r_eye = r_eye / 255
        r_eye = r_eye.reshape(24, 24, 1)
        r_eye = np.expand_dims(r_eye, axis=0)

        pred = model.predict(r_eye, verbose=0)
        rpred = np.argmax(pred, axis=1)
        break

    # LEFT EYE
    for (x, y, w, h) in left_eye:
        l_eye = frame[y:y+h, x:x+w]
        l_eye = cv2.cvtColor(l_eye, cv2.COLOR_BGR2GRAY)
        l_eye = cv2.resize(l_eye, (24, 24))
        l_eye = l_eye / 255
        l_eye = l_eye.reshape(24, 24, 1)
        l_eye = np.expand_dims(l_eye, axis=0)

        pred = model.predict(l_eye, verbose=0)
        lpred = np.argmax(pred, axis=1)
        break

    # Drowsiness logic
    if rpred[0] == 0 and lpred[0] == 0:
        score += 1
        status = "Closed"
    else:
        score -= 1
        status = "Open"

    if score < 0:
        score = 0

    # Display text
    cv2.putText(frame, status, (10, height-20), font, 1, (255, 255, 255), 1)
    cv2.putText(frame, "Score: " + str(score), (100, height-20), font, 1, (255, 255, 255), 1)

    # Alarm condition
    if score > 150:
        cv2.imwrite("image.jpg", frame)

        try:
            sound.play()
        except:
            pass

        if thicc < 16:
            thicc += 2
        else:
            thicc -= 2
            if thicc < 2:
                thicc = 2

        cv2.rectangle(frame, (0, 0), (width, height), (0, 0, 255), thicc)

    cv2.imshow("Driver Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()