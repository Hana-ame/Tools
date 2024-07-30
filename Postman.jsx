import React, { useState } from 'react';

function Postman() {
  const [url, setUrl] = useState('');
  const [method, setMethod] = useState('GET');
  const [headers, setHeaders] = useState('');
  const [body, setBody] = useState('');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);

  const handleRequest = async () => {
    setResponse(null);
    setError(null);
    const config = {
      method,
      headers: headers ? JSON.parse(headers) : {},
      body: method !== 'GET' ? (body || '') : null,
    };

    try {
      const res = await fetch(url, config);
      const data = await res.text();
      setResponse({ data, status: res.status, statusText: res.statusText });
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="App">
      <h1>HTTP Requester</h1>
      <input
        type="text"
        placeholder="Enter URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ width: '400px' }}
      />
      <select value={method} onChange={(e) => setMethod(e.target.value)}>
        <option value="GET">GET</option>
        <option value="POST">POST</option>
        <option value="PUT">PUT</option>
        <option value="DELETE">DELETE</option>
      </select>
      <br />
      <textarea
        placeholder="Headers (JSON format)"
        value={headers}
        onChange={(e) => setHeaders(e.target.value)}
        rows="4"
        style={{ width: '400px' }}
      />
      <textarea
        placeholder="Body (JSON format)"
        value={body}
        onChange={(e) => setBody(e.target.value)}
        rows="4"
        style={{ width: '400px' }}
      />
      <br />
      <button onClick={handleRequest}>Send Request</button>

      {response && (
        <div>
          <h2>Response:</h2>
          <pre>{response.data && (response.data)}</pre>
        </div>
      )}
      {error && (
        <div>
          <h2>Error:</h2>
          <pre>{error}</pre>
        </div>
      )}
    </div>
  );
}

export default Postman;