Landing.jsx 
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Landing() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    if (email && password) {
      // MVP-level validation
      navigate("/dashboard");
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gray-900">
      <div className="w-80 bg-gray-800 p-4 rounded-2xl shadow-lg">
        <h2 className="text-xl text-white font-semibold text-center mb-3">
          Manager Login
        </h2>

        <input
          type="email"
          placeholder="Enter email"
          className="w-full p-2 mb-2 bg-gray-700 text-white rounded-lg outline-none"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Enter password"
          className="w-full p-2 mb-3 bg-gray-700 text-white rounded-lg outline-none"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-medium"
          onClick={handleLogin}
        >
          Login
        </button>
      </div>
    </div>
  );
}
