import cv2
import os
from time import time
from PIL import Image
from tkinter import messagebox

def main_app(name, timeout=5):
    detector = cv2.dnn.readNetFromCaffe(
        "./data/deploy.prototxt",  
        "./data/res10_300x300_ssd_iter_140000.caffemodel"
    )
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    classifier_path = f"./public/classifiers/{name}_classifier.xml"
    
    if not os.path.exists(classifier_path):
        print(f"Error: Classifier file '{classifier_path}' not found.")
        messagebox.showerror('Error', 'Face recognition model not found!')
        return
    
    recognizer.read(classifier_path)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access webcam.")
        messagebox.showerror('Error', 'Cannot access webcam!')
        return
    
    pred = False
    start_time = time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from webcam.")
            break
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        color_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)  # Convert back to 3 channels
        
        (h, w) = gray_frame.shape[:2]
        blob = cv2.dnn.blobFromImage(color_frame, scalefactor=1.0, size=(300, 300), mean=(104.0, 177.0, 123.0))
        detector.setInput(blob)
        detections = detector.forward()
        
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * [w, h, w, h]
                (x, y, x_max, y_max) = box.astype("int")
                roi_gray = gray_frame[y:y_max, x:x_max]
                
                try:
                    id, conf = recognizer.predict(roi_gray)
                    conf = 100 - int(conf)
                    if conf > 50:
                        pred = True
                        text = f'Recognized: {name.upper()}'
                        color = (255, 255, 255)
                    else:
                        pred = False
                        text = "Unknown Face"
                        color = (0, 0, 0)
                except Exception as e:
                    print(f"Error during recognition: {e}")
                    continue
                
                cv2.rectangle(gray_frame, (x, y), (x_max, y_max), color, 2)
                cv2.putText(gray_frame, text, (x, y - 4), cv2.FONT_HERSHEY_PLAIN, 1, color, 1, cv2.LINE_AA)
        
        cv2.imshow("Face Recognition", gray_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        elapsed_time = time() - start_time
        if elapsed_time >= timeout:
            if pred:
                messagebox.showinfo('Congrat', 'You are a student of AGC')
            else:
                messagebox.showerror('Alert', 'You are not a student of AGC')
            break
    
    cap.release()
    cv2.destroyAllWindows()