import React, { useState, useRef, useEffect } from "react";
import Button from "@/components/ui/button";
import cv from "@techstark/opencv-js";

const FaceRecognition = () => {
  const [verificationResult, setVerificationResult] = useState(null);
  const videoRef = useRef(null);
  const captureCanvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const classifier = useRef(new cv.CascadeClassifier());

  // Load Haar Cascade Classifier
  useEffect(() => {
    const loadClassifier = async () => {
      await new Promise((resolve) => {
        classifier.current.load("/classifiers/Sushrut_classifier.xml", resolve);
      });
    };

    loadClassifier();
  }, []);

  // Start the webcam when the component mounts
  useEffect(() => {
    const startCamera = async () => {
      try {
        const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = mediaStream;
        }
        setStream(mediaStream);
      } catch (error) {
        console.error("Error accessing webcam:", error);
      }
    };

    startCamera();

    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop()); // Stop the camera when component unmounts
      }
    };
  }, []);

  // Capture image from video stream
  const capturePhoto = () => {
    const videoElement = videoRef.current;
    const canvasElement = captureCanvasRef.current;
    if (videoElement && canvasElement) {
      const ctx = canvasElement.getContext("2d");
      ctx.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
    }
  };

  // Function to verify the captured image using Haar Cascade Classifier
  const verifyUser = () => {
    const canvasElement = captureCanvasRef.current;
    if (!canvasElement) return;

    let src = cv.imread(canvasElement);
    let gray = new cv.Mat();
    cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY, 0);

    let facesArray = new cv.RectVector();
    classifier.current.detectMultiScale(gray, facesArray, 1.1, 3, 0, new cv.Size(100, 100), new cv.Size(300, 300));

    if (facesArray.size() === 0) {
      setVerificationResult("No face detected ❌");
      return;
    }

    // If the classifier detects a face, we assume it matches the trained data
    setVerificationResult("User Verified ✅");

    src.delete();
    gray.delete();
    facesArray.delete();
  };

  return (
    <div className="flex flex-col items-center gap-4 p-4">
      <video ref={videoRef} autoPlay className="border w-96 h-72"></video>
      <canvas ref={captureCanvasRef} width={500} height={500} className="hidden" />
      <Button onClick={capturePhoto}>Capture Photo</Button>
      <Button onClick={verifyUser}>Verify User</Button>
      {verificationResult && <p className="text-lg font-bold">{verificationResult}</p>}
    </div>
  );
};

export default FaceRecognition;
