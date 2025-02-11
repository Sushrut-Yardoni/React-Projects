import React, { useState, useContext, createContext } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import Webcam from "react-webcam";
import "./App.css"; // Make sure you have this file for styling

// Create a context for global state
const AppContext = createContext();

function App() {
  const [names, setNames] = useState([]);
  const [activeName, setActiveName] = useState("");
  const [numOfImages, setNumOfImages] = useState(0);

  return (
    <AppContext.Provider value={{ names, setNames, activeName, setActiveName, numOfImages, setNumOfImages }}>
      <Router>
        <Routes>
          <Route path="/" element={<StartPage />} />
          <Route path="/signup" element={<PageOne />} />
          <Route path="/check-user" element={<PageTwo />} />
          <Route path="/capture" element={<PageThree />} />
          <Route path="/recognize" element={<PageFour />} />
        </Routes>
      </Router>
    </AppContext.Provider>
  );
}

function StartPage() {
  const navigate = useNavigate();
  return (
    <div>
      <h1>Home Page</h1>
      <img src="homepagepic.png" alt="Home" style={{ width: 250, height: 250 }} />
      <div>
        <button onClick={() => navigate("/signup")}>Sign Up</button>
        <button onClick={() => navigate("/check-user")}>Check a User</button>
        <button onClick={() => window.confirm("Are you sure?") && window.close()}>Quit</button>
      </div>
    </div>
  );
}

function PageOne() {
  const { names, setNames, setActiveName } = useContext(AppContext);
  const [userName, setUserName] = useState("");
  const navigate = useNavigate();

  const startTraining = () => {
    if (!userName.trim() || userName === "None") {
      alert("Invalid name!");
      return;
    }
    if (names.includes(userName)) {
      alert("User already exists!");
      return;
    }
    setNames([...names, userName]);
    setActiveName(userName);
    navigate("/capture");
  };

  return (
    <div>
      <h2>Enter the name</h2>
      <input
        type="text"
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
        placeholder="Username"
      />
      <button onClick={() => navigate("/")}>Cancel</button>
      <button onClick={startTraining}>Next</button>
      <button onClick={() => setUserName("")}>Clear</button>
    </div>
  );
}

function PageTwo() {
  const { names, setActiveName } = useContext(AppContext);
  const [userName, setUserName] = useState("");
  const navigate = useNavigate();

  const nextFoo = () => {
    if (!userName.trim() || userName === "None") {
      alert("Invalid name!");
      return;
    }
    setActiveName(userName);
    navigate("/recognize");
  };

  return (
    <div>
      <h2>Enter your username</h2>
      <input
        type="text"
        value={userName}
        onChange={(e) => setUserName(e.target.value)}
        placeholder="Username"
      />
      <select onChange={(e) => setUserName(e.target.value)}>
        <option value="">Select a user</option>
        {names.map((name) => (
          <option key={name} value={name}>
            {name}
          </option>
        ))}
      </select>
      <button onClick={() => navigate("/")}>Cancel</button>
      <button onClick={nextFoo}>Next</button>
      <button onClick={() => setUserName("")}>Clear</button>
    </div>
  );
}

function PageThree() {
  const { activeName, numOfImages, setNumOfImages } = useContext(AppContext);
  const navigate = useNavigate();
  const webcamRef = React.useRef(null);

  const captureImages = () => {
    alert("We will capture 100 images of your face.");
    // Logic to capture images using webcamRef
    setNumOfImages(100);
  };

  const trainModel = () => {
    if (numOfImages < 100) {
      alert("Not enough data. Capture at least 100 images!");
      return;
    }
    alert("The model has been successfully trained!");
    navigate("/recognize");
  };

  return (
    <div>
      <h2>Capture Images</h2>
      <p>Number of images captured: {numOfImages}</p>
      <Webcam ref={webcamRef} />
      <button onClick={captureImages}>Capture Data Set</button>
      <button onClick={trainModel}>Train the Model</button>
    </div>
  );
}

function PageFour() {
  const { activeName } = useContext(AppContext);
  const navigate = useNavigate();

  const openWebcam = () => {
    alert(`Recognizing face for ${activeName}`);
  };

  return (
    <div>
      <h2>Face Recognition</h2>
      <button onClick={openWebcam}>Face Recognition</button>
      <button onClick={() => navigate("/")}>Go to Home Page</button>
    </div>
  );
}

export default App;
