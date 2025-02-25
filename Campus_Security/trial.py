import cv2
import os

# Load OpenCV's deep learning face detection model
face_net = cv2.dnn.readNetFromCaffe(
    "./data/deploy.prototxt",  
    "./data/res10_300x300_ssd_iter_140000.caffemodel"  
)

# Function to detect the largest face using DNN
def detect_largest_face(frame):
    h, w = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_net.setInput(blob)
    detections = face_net.forward()

    largest_face = None
    max_area = 0

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Confidence threshold
            box = detections[0, 0, i, 3:7] * [w, h, w, h]
            (x, y, x_max, y_max) = box.astype("int")

            # Calculate face area
            area = (x_max - x) * (y_max - y)
            if area > max_area:
                max_area = area
                largest_face = (x, y, x_max - x, y_max - y)  # Store largest face

    return largest_face

# Function to capture 100 images and save to dataset
def capture_images(name):
    path = "./data/" + name
    os.makedirs(path, exist_ok=True)  # Create folder if it doesn't exist

    cap = cv2.VideoCapture(0)  # Open webcam
    if not cap.isOpened():
        print("❌ Error: Could not open webcam.")
        return

    num_images = 0

    while num_images < 100:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Could not read frame.")
            break

        largest_face = detect_largest_face(frame)

        if largest_face:
            x, y, w, h = largest_face
            face_img = frame[y:y+h, x:x+w]  # Extract face region

            if face_img.size > 0:
                face_img = cv2.resize(face_img, (200, 200))  # Resize for consistency
                file_path = os.path.join(path, f"{num_images}.jpg")
                cv2.imwrite(file_path, face_img)  # Save face image
                num_images += 1

                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Captured: {num_images}/100", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Face Capture", frame)

        # Press 'q' to exit early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ {num_images} images captured and saved in {path}")

# Run the function to capture images
user_name = input("Enter your name: ")
capture_images(user_name)
