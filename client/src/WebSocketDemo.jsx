import React, { useState } from 'react';

const WebSocketDemo = () => {
  const [responseChunks, setResponseChunks] = useState([]);
  const [inputText, setInputText] = useState('');

  const handleSend = () => {
    const url = 'http://127.0.0.1:8000/review-code';

    const eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
      const response = JSON.parse(event.data);
      console.log(response); // Log the stream response
    };

    eventSource.onerror = (error) => {
      console.error('Error:', error);
    };
  };

  return (
    <div>
      <h1>OpenAI Response as Chunks</h1>
      <button onClick={handleSend}>Send</button>
      {/* <div>
        {responseChunks.map((chunk, index) => (
          <p key={index}>{chunk}</p>
        ))}
      </div> */}
    </div>
  );
};

export default WebSocketDemo;
