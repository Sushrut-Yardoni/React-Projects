import React, { useState } from "react";
import "./ChatApp.css";

function ChatApp() {
  const [users, setUsers] = useState([]);
  const [currentUser, setCurrentUser] = useState("");
  const [messages, setMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");

  const handleSignUp = (name) => {
    if (name && !users.includes(name)) {
      setUsers([...users, name]);
      setCurrentUser(name);
    } else {
      alert("Username is invalid or already taken.");
    }
  };

  const handleSendMessage = () => {
    if (chatInput.trim()) {
      setMessages([...messages, { user: currentUser, text: chatInput }]);
      setChatInput("");
    }
  };

  return (
    <div className="chat-app">
      {!currentUser ? (
        <div className="signup-container">
          <h2>Create an Account</h2>
          <input
            type="text"
            placeholder="Enter your name"
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSignUp(e.target.value);
            }}
          />
          <button
            onClick={(e) =>
              handleSignUp(e.target.previousSibling.value)
            }
          >
            Sign Up
          </button>
        </div>
      ) : (
        <div className="chat-container">
          <h2>Welcome, {currentUser}!</h2>
          <div className="chat-box">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`message ${
                  msg.user === currentUser ? "my-message" : "friend-message"
                }`}
              >
                <strong>{msg.user}: </strong>
                {msg.text}
              </div>
            ))}
          </div>
          <div className="chat-input">
            <input
              type="text"
              placeholder="Type a message"
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleSendMessage();
              }}
            />
            <button onClick={handleSendMessage}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default ChatApp;
