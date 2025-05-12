import cv2
import numpy as np
import os

def capture_iris_image(filename='user_data/current.jpg'):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        eyes = eyes_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in eyes:
            iris = frame[y:y + h, x:x + w]
            cv2.imwrite(filename, iris)
            cap.release()
            return filename

        cv2.imshow('Scan your eye', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

def compare_iris(img1_path, img2_path):
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        return False

    img1 = cv2.resize(img1, (100, 100))
    img2 = cv2.resize(img2, (100, 100))

    diff = cv2.absdiff(img1, img2)
    score = np.mean(diff)

    print(f"Match score: {score}")
    return score < 15  # Threshold — lower is more similar
