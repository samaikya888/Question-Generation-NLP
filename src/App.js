import React, {useEffect, useState } from 'react';
import './App.css'

const App = () => {
  const [isTextMode, setIsTextMode] = useState(true);
  const [text, setText] = useState('');
  const [pdfFile, setPdfFile] = useState(null);
  const [submit,setSubmit] = useState(false);
  const [resp, setResp] = useState(null);
  let responseData = null;

  useEffect(() => {
    console.log("in effect")
    console.log(resp)
  }, [resp]);

  // const fetchData = async () => {
  //   try {
  //     const response = await fetch('/api/data');
  //     const jsonData = await response.json();
  //     // setData(jsonData);
  //   } catch (error) {
  //     console.error('Error occurred while fetching data:', error);
  //   }
  // };

  const handleToggle = () => {
    setIsTextMode(!isTextMode);
  };

  const handleTextChange = (e) => {
    setText(e.target.value);
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    setPdfFile(file);
  };

  const sendData = async () => {
    try {
      const formData = new FormData();
      formData.append('isTextMode', isTextMode);
      
      if (isTextMode) {
        formData.append('text', text);
      } 
      else {
        formData.append('pdfFile', pdfFile);
      }

      console.log(formData);

      var response = await fetch('http://127.0.0.1:5000/api/endpoint', {
        method: 'POST',
        body: formData
      });

      setResp(await response.json());

      setSubmit(true);

      // Handle the response from the backend
      // if (response.ok) {
      //   console.log('Data sent successfully!');
      //   setSubmit(true);
        
      // } else {
      //   console.error('Failed to send data.');
      // }
    } catch (error) {
      console.error('Error occurred while sending data:', error);
    }
  };

  return (
    <div className="container">
      { !submit && (
      <div>
      <h1>Text or PDF Upload</h1>
      <div className="toggle-container">
        <button className={`toggle-button ${isTextMode ? 'active' : ''}`} onClick={handleToggle}>
          Text Input
        </button>
        <button className={`toggle-button ${!isTextMode ? 'active' : ''}`} onClick={handleToggle}>
          PDF Upload
        </button>
      </div>
      
      {isTextMode ? (
        <div className="input-container">
          <label htmlFor="text-input">Enter Text:</label>
          <textarea
            id="text-input"
            value={text}
            onChange={handleTextChange}
            className="text-area"
          />
        </div>
      ) : (
        <div className="input-container">
          <label htmlFor="file-input">Upload PDF:</label>
          <input
            id="file-input"
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
          />
        </div>
      )}
      <div className="preview-container">
        <h2>Preview:</h2>
        {isTextMode ? (
          <div className="text-preview">
            <p>{text}</p>
          </div>
        ) : (
          <div className="pdf-preview">
            {pdfFile && (
              <embed
                src={URL.createObjectURL(pdfFile)}
                type="application/pdf"
                width="100%"
                height="500px"
              />
            )}
          </div>
        )}
      </div>
    <div> <button onClick={sendData}>Submit</button> </div>
    </div>
    )}
    {submit && (
      <div>
        {resp ? (
        <div>
          <ul className="question-list">
            {resp.map((item, index) => (
              <li key={index}>
                <h3>Question: {item.question}</h3>
                <p>Options:
                  <ol className="options-list">
                    {item.options.map((option, i) => (
                      <li key={i}>
                        {option}
                      </li>
                    ))}
                  </ol>
                </p>
                <p>Answer: {item.answer}</p>
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p>Loading data...</p>
      )}
      </div>
    )}
    </div>
  );
};

export default App;
