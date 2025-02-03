import React, { useEffect, useRef, useState } from "react";
import * as faceapi from "face-api.js";

const FaceRecognition = ({ name }) => {
  const videoRef = useRef(null);
  const [recognized, setRecognized] = useState(false);

  useEffect(() => {
    const loadModels = async () => {
      await faceapi.nets.tinyFaceDetector.loadFromUri("/models");
      await faceapi.nets.faceRecognitionNet.loadFromUri("/models");
      await faceapi.nets.faceLandmark68Net.loadFromUri("/models");
      startVideo();
    };

    const startVideo = () => {
      navigator.mediaDevices
        .getUserMedia({ video: {} })
        .then((stream) => {
          videoRef.current.srcObject = stream;
        })
        .catch((err) => console.error("Error accessing webcam:", err));
    };

    loadModels();
  }, []);

  useEffect(() => {
    const recognizeFace = async () => {
      const labeledDescriptors = await loadLabeledImages();
      const faceMatcher = new faceapi.FaceMatcher(labeledDescriptors, 0.6);

      setInterval(async () => {
        const detections = await faceapi
          .detectAllFaces(videoRef.current, new faceapi.TinyFaceDetectorOptions())
          .withFaceLandmarks()
          .withFaceDescriptors();

        const results = detections.map((d) => faceMatcher.findBestMatch(d.descriptor));

        results.forEach((result) => {
          if (result.label === name) {
            setRecognized(true);
          }
        });
      }, 2000);
    };

    recognizeFace();
  }, [name]);

  const loadLabeledImages = () => {
    const labels = [name];
    return Promise.all(
      labels.map(async (label) => {
        const descriptions = [];
        for (let i = 1; i <= 2; i++) {
          const img = await faceapi.fetchImage(`/data/${label}/${i}.jpg`);
          const detections = await faceapi.detectSingleFace(img).withFaceLandmarks().withFaceDescriptor();
          descriptions.push(detections.descriptor);
        }
        return new faceapi.LabeledFaceDescriptors(label, descriptions);
      })
    );
  };

  return (
    <div>
      <h2>{recognized ? `Recognized: ${name}` : "Unknown Face"}</h2>
      <video ref={videoRef} autoPlay muted width="720" height="560"></video>
    </div>
  );
};

export default FaceRecognition;
