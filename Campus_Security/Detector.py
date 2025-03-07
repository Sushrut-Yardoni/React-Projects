import cv2
import os
from time import time
from tkinter import messagebox
import numpy as np

def draw_ar_overlay(frame, x, y, x_max, y_max, color):
    """Draws a futuristic AR-style overlay around detected faces."""
    thickness = 2
    corner_length = 15
    
    # Draw corner elements
    cv2.line(frame, (x, y), (x + corner_length, y), color, thickness)
    cv2.line(frame, (x, y), (x, y + corner_length), color, thickness)
    
    cv2.line(frame, (x_max, y), (x_max - corner_length, y), color, thickness)
    cv2.line(frame, (x_max, y), (x_max, y + corner_length), color, thickness)
    
    cv2.line(frame, (x, y_max), (x + corner_length, y_max), color, thickness)
    cv2.line(frame, (x, y_max), (x, y_max - corner_length), color, thickness)
    
    cv2.line(frame, (x_max, y_max), (x_max - corner_length, y_max), color, thickness)
    cv2.line(frame, (x_max, y_max), (x_max, y_max - corner_length), color, thickness)
    
    # Vertical scanning line effect from top to bottom
    scan_y = int(y + ((time() % 1) * (y_max - y)))  # Moves from top to bottom
    cv2.line(frame, (x, scan_y), (x_max, scan_y), color, 1)

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
        
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
        detector.setInput(blob)
        detections = detector.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * [w, h, w, h]
                (x, y, x_max, y_max) = box.astype("int")
                roi_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)[y:y_max, x:x_max]
                
                try:
                    id, conf = recognizer.predict(roi_gray)
                    conf = 100 - int(conf)
                    if conf > 50:
                        pred = True
                        text = f'Recognized: {name.upper()}'
                        color = (255, 255, 0)  # Futuristic cyan
                    else:
                        pred = False
                        text = "Unknown Face"
                        color = (0, 0, 255)  # Red for unrecognized
                except Exception as e:
                    print(f"Error during recognition: {e}")
                    continue

                draw_ar_overlay(frame, x, y, x_max, y_max, color)
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow("Face Recognition", frame)
        
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