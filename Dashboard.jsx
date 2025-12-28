import React, { useState } from "react";
import { db } from "./firebase"; 
import { collection, addDoc } from "firebase/firestore";

export default function Dashboard() {
  const [projectName, setProjectName] = useState("");
  const [tools, setTools] = useState("");
  const [links, setLinks] = useState("");
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    try {
      await addDoc(collection(db, "projects"), {
        projectName: projectName,
        tools: tools.toLowerCase(), 
        links: links, // comma-separated string of URLs
        createdAt: new Date().toISOString(),
      });

      setStatus("Config uploaded successfully!");
      setTimeout(() => setStatus(""), 3000);
    } catch (err) {
      console.error(err);
      setStatus("Upload failed!");
    }
  };

  return (
    <div className="h-screen bg-gray-900 text-white flex justify-center items-center">
      <div className="w-96 bg-gray-800 p-5 rounded-2xl shadow-md">
        <h2 className="text-2xl font-semibold text-center mb-4">
          Manager Dashboard (MVP)
        </h2>

        <input
          type="text"
          placeholder="Project Name"
          className="w-full p-2 mb-2 bg-gray-700 rounded-lg outline-none"
          value={projectName}
          onChange={(e) => setProjectName(e.target.value)}
        />

        <textarea
          placeholder="Tools list (comma-separated)"
          className="w-full p-2 mb-2 bg-gray-700 rounded-lg outline-none"
          rows={3}
          value={tools}
          onChange={(e) => setTools(e.target.value)}
        ></textarea>

        <textarea
          placeholder="Source URLs (comma-separated)"
          className="w-full p-2 mb-3 bg-gray-700 rounded-lg outline-none"
          rows={4}
          value={links}
          onChange={(e) => setLinks(e.target.value)}
        ></textarea>

        <button
          className="w-full bg-green-600 hover:bg-green-700 py-2 rounded-lg font-medium"
          onClick={handleUpload}
        >
          Upload Config
        </button>

        {status && (
          <p className="text-center text-sm text-gray-300 mt-3">{status}</p>
        )}
      </div>
    </div>
  );
}
