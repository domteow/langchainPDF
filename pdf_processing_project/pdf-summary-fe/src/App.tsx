import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [summary, setSummary] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!file) {
      alert('Please select a PDF file.');
      return;
    }
  
    setLoading(true);
    const formData = new FormData();
    formData.append('pdf_file', file);

    const headers = new Headers();
    headers.append('Content-Type', 'multipart/form-data');
    console.log(formData.get('pdfFile'));

    // Send formData to your backend API using fetch or Axios
    try {
      const response = await fetch('http://127.0.0.1:8000/upload-pdf/', {
        method: 'POST',
        body: formData,
        // headers: headers,
      });
      // Handle the response from the server
      if (response.ok) {
        // Response is successful, handle it here
        const data = await response.json();
        console.log(data);
      } else {
        // Response has an error status, handle it here
        console.error('Error:', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Error uploading PDF:', error);
    }
    setLoading(false);
  
  };
  
        

  return (
    <div className="App">
    <h1>PDF Summary Generator</h1>
    <form encType="multipart/form-data" onSubmit={handleSubmit}>
      <div className="file-upload">
        <input type="file" name="pdf_file" accept=".pdf" onChange={handleFileChange} />
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Generate Summary'}
        </button>
      </div>
    </form>
    {summary && (
      <div className="summary">
        <h2>Summary:</h2>
        <p>{summary}</p>
      </div>
    )}
  </div>
  );
}

export default App;
