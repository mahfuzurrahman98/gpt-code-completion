import axios from 'axios';
import { useState } from 'react';
import './App.css';

function App() {
  const [response, setResponse] = useState('');
  const url = 'http://127.0.0.1:8000/get_names_chunked';
  const handleClick = async () => {

    // send an HTTP request to the server API
    try {
      // now fetch the data as a stream and set the response on the state so it can be displayed look like writing real time
      const res = await axios.get(url, { responseType: 'stream' });

      // create a reader to read the stream
      const reader = res.data.getReader();

// now read the stream make it string and set it on the state

      const stream = new ReadableStream({
        start(controller) {
          // The following function handles each data chunk
          function push() {
            // "done" is a Boolean and value a "Uint8Array"
            reader.read().then(({ done, value }) => {
              // Is there no more data to read?
              if (done) {
                // Tell the browser that we have finished sending data
                controller.close();
                return;
              }

              // Get the data and send it to the browser via the controller
              controller.enqueue(value);
              push();
            });
          }

          push();
        },
      });

      // Respond with our stream

      const readableStream = new Response(stream);
      const data = await readableStream.text();
      setResponse(data);



      
      
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div>
      <button onClick={handleClick}>get</button>
      <p>{response}</p>
    </div>
  );
}

export default App;
