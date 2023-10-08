import { useState } from 'react';
import './App.css';
import WevbSocketDemo from './WebSocketDemo';

function App() {
  const [response, setResponse] = useState('');
  const url = 'http://127.0.0.1:8000/get_names_chunked';

  
  return (
    <WevbSocketDemo />
  );
}

export default App;
