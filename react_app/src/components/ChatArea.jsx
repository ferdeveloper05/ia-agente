import React, { useState, useEffect, useRef } from 'react';

function ChatArea({ currentConversation, addMessage }) {
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const endOfMessagesRef = useRef(null);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [currentConversation?.messages, isTyping]);

  if (!currentConversation) return <div className="main-area"></div>;

  const simulateAiResponse = (prompt) => {
    setIsTyping(true);
    setTimeout(() => {
      const response = `Esta es una respuesta simulada a tu mensaje: '${prompt}'. Más adelante se conectará con el LLM.`;
      addMessage(response, 'assistant');
      setIsTyping(false);
    }, 1000);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || isTyping) return;
    
    const userPrompt = input.trim();
    addMessage(userPrompt, 'user');
    setInput('');
    
    simulateAiResponse(userPrompt);
  };

  return (
    <div className="main-area">
      <div className="chat-container">
        <div className="chat-title">
          🤖 Bienvenido a tu chatbot de IA Sirpef
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
