import React, { useEffect, useState } from 'react';
import * as faceapi from 'face-api.js';

const TrainClassifier = ({ name }) => {
  const [trainingStatus, setTrainingStatus] = useState('');

  useEffect(() => {
    const loadModelsAndTrain = async () => {
      try {
        // Load face-api.js models
        await faceapi.nets.faceRecognitionNet.loadFromUri('/models');
        await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
        await faceapi.nets.ssdMobilenetv1.loadFromUri('/models');

        // Load images and labels
        const labeledFaceDescriptors = await loadLabeledImages(name);

        // Train the classifier
        const faceMatcher = new faceapi.FaceMatcher(labeledFaceDescriptors, 0.6);
        setTrainingStatus('Training completed successfully!');
        console.log('Classifier trained:', faceMatcher);
      } catch (error) {
        console.error('Error during training:', error);
        setTrainingStatus('Training failed. Check console for details.');
      }
    };

    loadModelsAndTrain();
  }, [name]);

  const loadLabeledImages = async (name) => {
    const path = `./data/${name}/`;
    const labels = [];
    const descriptions = [];

    // Fetch images and labels
    const files = await fetchImageFiles(path);

    for (const file of files) {
      const img = await faceapi.fetchImage(`${path}${file}`);
      const detections = await faceapi
        .detectSingleFace(img)
        .withFaceLandmarks()
        .withFaceDescriptor();

      if (detections) {
        const label = file.split(name)[0]; // Extract label from filename
        labels.push(label);
        descriptions.push(detections.descriptor);
      }
    }

    return labels.map((label, i) => {
      return new faceapi.LabeledFaceDescriptors(label, [descriptions[i]]);
    });
  };

  const fetchImageFiles = async (path) => {
    // Simulate fetching files from a directory
    // In a real app, you might use an API or file system access
    return ['1_tho1.jpg', '2_tho1.jpg', '3_tho1.jpg']; // Example filenames
  };

  return (
    <div>
      <h1>Training Classifier for {name}</h1>
      <p>{trainingStatus}</p>
    </div>
  );
};

export default TrainClassifier;