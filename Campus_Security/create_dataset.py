import cv2
import os

def start_capture(name):
    path = f"./data/{name}"
    num_of_images = 0

    # Load pre-trained model
    detector = cv2.dnn.readNetFromCaffe(
        "./data/deploy.prototxt",
        "./data/res10_300x300_ssd_iter_140000.caffemodel"
    )

    os.makedirs(path, exist_ok=True)  # Create directory if not exists

    vid = cv2.VideoCapture(0)
    if not vid.isOpened():
        print("Error: Cannot access webcam.")
        return 0

    while num_of_images < 100:
        ret, img = vid.read()
        if not ret:
            break

        # Prepare image for DNN model
        (h, w) = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, scalefactor=1.0, size=(300, 300), mean=(104.0, 177.0, 123.0))
        detector.setInput(blob)
        detections = detector.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # Confidence threshold
                box = detections[0, 0, i, 3:7] * [w, h, w, h]
                (x, y, x_max, y_max) = box.astype("int")

                cv2.rectangle(img, (x, y), (x_max, y_max), (0, 255, 0), 2)
                cv2.putText(img, "Face Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0))
                cv2.putText(img, f"{num_of_images} images captured", (x, y_max + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0))

                face_img = img[y:y_max, x:x_max]
                if face_img.size > 0:  # Ensure valid face crop
                    cv2.imwrite(str(path+"/"+str(num_of_images)+name+".jpg"), face_img)
                    num_of_images += 1

        cv2.imshow("Face Detection", img)
        if cv2.waitKey(1) & 0xFF in [ord("q"), 27]:  # Stop on 'q' or 'Esc'
            break

    vid.release()
    cv2.destroyAllWindows()
    return num_of_images


def take_video(name, video_path):
    path = f"./data/{name}"
    num_of_images = 0

    # Load pre-trained model
    detector = cv2.dnn.readNetFromCaffe(
        "./data/deploy.prototxt",
        "./data/res10_300x300_ssd_iter_140000.caffemodel"
    )

    os.makedirs(path, exist_ok=True)

    vid = cv2.VideoCapture(video_path)
    if not vid.isOpened():
        print("Error: Could not open video file.")
        return 0

    while num_of_images < 100:
        ret, img = vid.read()
        if not ret:
            break

        # Prepare image for DNN model
        (h, w) = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, scalefactor=1.0, size=(300, 300), mean=(104.0, 177.0, 123.0))
        detector.setInput(blob)
        detections = detector.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:  # Confidence threshold
                box = detections[0, 0, i, 3:7] * [w, h, w, h]
                (x, y, x_max, y_max) = box.astype("int")

                cv2.rectangle(img, (x, y), (x_max, y_max), (0, 255, 0), 2)
                cv2.putText(img, "Face Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0))
                cv2.putText(img, f"{num_of_images} images captured", (x, y_max + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0))

                face_img = img[y:y_max, x:x_max]
                if face_img.size > 0:  # Ensure valid face crop
                    cv2.imwrite(str(path+"/"+str(num_of_images)+name+".jpg"), face_img)
                    num_of_images += 1

        cv2.imshow("Face Detection", img)
        if cv2.waitKey(1) & 0xFF in [ord("q"), 27]:  # Stop on 'q' or 'Esc'
            break

    vid.release()
    cv2.destroyAllWindows()
    return num_of_images

# Example usage:
# take_video('tho1', 'data/WIN_20230920_07_56_11_Pro.mp4')
