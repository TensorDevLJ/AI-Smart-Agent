import React, {useState, useEffect, useRef} from 'react';
import axios from 'axios';
import { API_BASE } from './config';
import './App.css';

function App(){
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const boxRef = useRef(null);

  useEffect(() => {
    if(boxRef.current) boxRef.current.scrollTop = boxRef.current.scrollHeight;
  }, [messages]);

  const send = async () => {
    if(!input.trim()) return;
    const userMsg = {sender:'user', text: input};
    setMessages(prev => [...prev, userMsg]);
    try{
      const res = await axios.post(`${API_BASE}/ask`, {message: input});
      const bot = {sender:'bot', text: res.data.reply};
      setMessages(prev => [...prev, bot]);
    }catch(e){
      const bot = {sender:'bot', text: '⚠️ Could not reach backend.'};
      setMessages(prev => [...prev, bot]);
    }
    setInput('');
  };

  const onKey = (e) => { if(e.key === 'Enter') send(); }

  return (
    <div className="app">
      <div className="chat-card">
        <h2>🤖 Smart Agent</h2>
        <div className="messages" ref={boxRef}>
          {messages.map((m,i) => (
            <div key={i} className={'msg ' + m.sender}>
              {m.text}
            </div>
          ))}
        </div>
        <div className="input-area">
          <input value={input} onChange={(e)=>setInput(e.target.value)} onKeyDown={onKey} placeholder="Type a command, e.g., 'Remind me to call mom at 6pm'"/>
          <button onClick={send}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
