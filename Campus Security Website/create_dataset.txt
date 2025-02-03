import React, { useRef, useState, useEffect } from "react";
import Webcam from "react-webcam";
import * as cv from "opencv.js";

const FaceCapture = ({ name }) => {
  const webcamRef = useRef(null);
  const [numOfImages, setNumOfImages] = useState(0);
  const [capturing, setCapturing] = useState(false);

  useEffect(() => {
    if (capturing) {
      const interval = setInterval(() => captureFrame(), 100);
      return () => clearInterval(interval);
    }
  }, [capturing]);

  const captureFrame = () => {
    if (!webcamRef.current) return;
    const imageSrc = webcamRef.current.getScreenshot();
    const img = new Image();
    img.src = imageSrc;
    img.onload = () => processImage(img);
  };

  const processImage = (img) => {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0, img.width, img.height);
    const gray = new cv.Mat();
    const src = cv.imread(canvas);
    cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY, 0);
    const faces = new cv.RectVector();
    const faceCascade = new cv.CascadeClassifier();
    faceCascade.load("haarcascade_frontalface_default.xml");
    faceCascade.detectMultiScale(gray, faces, 1.1, 5, 0);
    if (faces.size() > 0) {
      saveImage(imageSrc);
    }
    src.delete();
    gray.delete();
    faces.delete();
    faceCascade.delete();
  };

  const saveImage = (imageSrc) => {
    setNumOfImages((prev) => prev + 1);
    const link = document.createElement("a");
    link.href = imageSrc;
    link.download = `${name}_${numOfImages}.jpg`;
    link.click();
  };

  return (
    <div>
      <Webcam ref={webcamRef} screenshotFormat="image/jpeg" />
      <p>{numOfImages} images captured</p>
      <button onClick={() => setCapturing(true)}>Start Capture</button>
      <button onClick={() => setCapturing(false)}>Stop Capture</button>
    </div>
  );
};

export default FaceCapture;
