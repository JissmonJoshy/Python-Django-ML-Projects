import cv2

def fun2(data):

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')

    faceCascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    # Correct mapping
    id_to_name = {item['id']: item['name'] for item in data}

    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)

    minW = 0.2 * cam.get(3)
    minH = 0.2 * cam.get(4)

    results = []

    while len(results) < 10:  # 🔥 MULTI-FRAME CHECK
        ret, img = cam.read()
        if not ret:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=7,
            minSize=(int(minW), int(minH))
        )

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]

            label, confidence = recognizer.predict(face)

            print("ID:", label, "Confidence:", confidence)

            # 🔥 RELAXED BUT SAFE THRESHOLD
            if confidence < 60:
                results.append(label)
            else:
                results.append("unknown")

    cam.release()
    cv2.destroyAllWindows()

    # 🔥 MAJORITY VOTE
    if results.count("unknown") > 5:
        return "unknown"

    return max(set(results), key=results.count)