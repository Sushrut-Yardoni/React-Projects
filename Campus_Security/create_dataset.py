import cv2
import os
import numpy as np

def draw_futuristic_overlay(img, x, y, x_max, y_max, color):
    """Draws a futuristic AR-style overlay for face detection."""
    thickness = 2
    corner_length = 20
    
    # Corner markers
    cv2.line(img, (x, y), (x + corner_length, y), color, thickness)
    cv2.line(img, (x, y), (x, y + corner_length), color, thickness)
    
    cv2.line(img, (x_max, y), (x_max - corner_length, y), color, thickness)
    cv2.line(img, (x_max, y), (x_max, y + corner_length), color, thickness)
    
    cv2.line(img, (x, y_max), (x + corner_length, y_max), color, thickness)
    cv2.line(img, (x, y_max), (x, y_max - corner_length), color, thickness)
    
    cv2.line(img, (x_max, y_max), (x_max - corner_length, y_max), color, thickness)
    cv2.line(img, (x_max, y_max), (x_max, y_max - corner_length), color, thickness)
    
    # Scanning line effect
    scan_y = int(y + ((cv2.getTickCount() % cv2.getTickFrequency()) / cv2.getTickFrequency()) * (y_max - y))
    cv2.line(img, (x, scan_y), (x_max, scan_y), color, 1)

def start_capture(name):
    path = f"./data/{name}"
    num_of_images = 0

    detector = cv2.dnn.readNetFromCaffe(
        "./data/deploy.prototxt",
        "./data/res10_300x300_ssd_iter_140000.caffemodel"
    )

    os.makedirs(path, exist_ok=True)
    vid = cv2.VideoCapture(0)
    if not vid.isOpened():
        print("Error: Cannot access webcam.")
        return 0

    while num_of_images < 100:
        ret, img = vid.read()
        if not ret:
            break

        (h, w) = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, scalefactor=1.0, size=(300, 300), mean=(104.0, 177.0, 123.0))
        detector.setInput(blob)
        detections = detector.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * [w, h, w, h]
                (x, y, x_max, y_max) = box.astype("int")
                
                color = (255, 255, 0)  # Futuristic cyan color
                draw_futuristic_overlay(img, x, y, x_max, y_max, color)
                
                cv2.putText(img, "Face Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                cv2.putText(img, f"{num_of_images} images captured", (x, y_max + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
                
                face_img = img[y:y_max, x:x_max]
                if face_img.size > 0:
                    cv2.imwrite(str(path+"/"+str(num_of_images)+name+".jpg"), face_img)
                    num_of_images += 1

        cv2.imshow("Futuristic Face Detection", img)
        if cv2.waitKey(1) & 0xFF in [ord("q"), 27]:
            break

    vid.release()
    cv2.destroyAllWindows()
    return num_of_images
