import React, { useState, useEffect, useRef } from 'react';

function ChatArea({ conversationId, currentConversation, userName, addMessage }) {
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const endOfMessagesRef = useRef(null);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [currentConversation?.messages, isTyping]);

  if (!currentConversation) return <div className="main-area"></div>;

  const sendToBackend = async (prompt) => {
    setIsTyping(true);
    try {
      const res = await fetch('http://localhost:8000/api/v1/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: conversationId,
          question: prompt
        })
      });

      if (!res.ok) {
        const errText = await res.text();
        addMessage(`Error del servidor (${res.status}): ${errText}`, 'assistant');
        setIsTyping(false);
        return;
      }

      const data = await res.json();
      addMessage(data.response, 'assistant');
    } catch (err) {
      addMessage(`No se pudo conectar con el servidor: ${err.message}`, 'assistant');
    } finally {
      setIsTyping(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;
    
    const userPrompt = input.trim();
    addMessage(userPrompt, 'user');
    setInput('');
    
    sendToBackend(userPrompt);
  };

  return (
    <div className="main-area">
      <div className="chat-container">
        <div className="chat-title">
          🤖 Bienvenido{userName ? ` ${userName}` : ''} a tu chatbot de IA Sirpef
        </div>

        <div className="chat-content">
          {currentConversation.messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="avatar">
                {msg.role === 'assistant' ? '🤖' : '👤'}
              </div>
              <div className="content">
                {msg.content}
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="message assistant">
              <div className="avatar">🤖</div>
              <div className="content">Escribiendo...</div>
            </div>
          )}
          <div ref={endOfMessagesRef} />
        </div>
      </div>

      <div className="input-container">
        <form className="input-wrapper" onSubmit={handleSubmit}>
          <input 
            type="text" 
            className="chat-input"
            placeholder="Escribe tu mensaje..." 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isTyping}
          />
          <button type="submit" className="chat-submit" disabled={isTyping || !input.trim()}>
            {/* simple send icon or emoji */}
            ➤
          </button>
        </form>
      </div>
    </div>
  );
}

export default ChatArea;
