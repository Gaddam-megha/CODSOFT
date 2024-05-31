import cv2

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
        cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]
    return coords

def detect(img, faceCascade, eyeCascade, noseCascade, mouthCascade):
    color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 255, 0), "white": (255, 255, 255)}
    coords = draw_boundary(img, faceCascade, 1.1, 10, color['blue'], "Face")
    if len(coords) == 4:
        roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
        draw_boundary(roi_img, eyeCascade, 1.1, 12, color['red'], "Eye")
        draw_boundary(roi_img, noseCascade, 1.1, 4, color['green'], "Nose")
        draw_boundary(roi_img, mouthCascade, 1.1, 20, color['white'], "Mouth")
    return img

faceCascade = cv2.CascadeClassifier('C:/Users/Vaishnavi/AppData/Local/Programs/Python/Python312/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml')
eyesCascade = cv2.CascadeClassifier('C:/Users/Vaishnavi/AppData/Local/Programs/Python/Python312/Lib/site-packages/cv2/data/haarcascade_eye.xml')
noseCascade = cv2.CascadeClassifier('C:/Users/Vaishnavi/Dropbox/PC/Downloads/haarcascade_mcs_mouth.xml')
mouthCascade = cv2.CascadeClassifier('C:/Users/Vaishnavi/Dropbox/PC/Downloads/haarcascade_mcs_mouth.xml')

if faceCascade.empty() or eyesCascade.empty() or noseCascade.empty() or mouthCascade.empty():
    raise IOError("Could not load one or more Haar cascade classifiers")

try:
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, img = video_capture.read()
        if not ret:
            break
        img = detect(img, faceCascade, eyesCascade, noseCascade, mouthCascade)
        cv2.imshow("Face Detection", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    video_capture.release()
    cv2.destroyAllWindows()
