import cv2

def fun(face_id):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    count = 0

    while True:
        ret, img = cam.read()
        if not ret:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_detector.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=7,
            minSize=(80, 80)
        )

        for (x, y, w, h) in faces:
            if w < 80 or h < 80:
                continue

            face = gray[y:y+h, x:x+w]
            face = cv2.equalizeHist(face)

            count += 1

            cv2.imwrite(f"dataset/User.{face_id}.{count}.jpg", face)

            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Capturing Faces', img)

        if cv2.waitKey(1) == 27 or count >= 100:
            break

    cam.release()
    cv2.destroyAllWindows()