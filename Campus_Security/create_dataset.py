import cv2
import os

def start_capture(name):
    path = f"./data/{name}"
    num_of_images = 0
    os.makedirs(path, exist_ok=True)
    vid = cv2.VideoCapture(0)
    if not vid.isOpened():
        print("Error: Cannot access webcam.")
        return 0
    
    while num_of_images < 100:
        ret, img = vid.read()
        if not ret:
            break
        
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_img = gray_img
        if face_img.size > 0:
            cv2.imwrite(str(path+"/"+str(num_of_images)+name+".jpg"), face_img)
            num_of_images += 1
        
        cv2.imshow("Grayscale Image Capture", gray_img)
        if cv2.waitKey(1) & 0xFF in [ord("q"), 27]:
            break
    
    vid.release()
    cv2.destroyAllWindows()
    return num_of_images