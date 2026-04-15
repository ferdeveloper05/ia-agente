import React, { useState } from 'react';

function EmailModal({ onClose }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [success, setSuccess] = useState(false);

  const handleConnect = () => {
    if (email && password) {
      setSuccess(true);
      setTimeout(() => {
        onClose();
      }, 1500);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <h3>Conectar Correo Electrónico</h3>
        
        {success ? (
          <div style={{ color: '#00cc66', padding: '1rem 0' }}>
            Correo {email} conectado (Simulado)!
          </div>
        ) : (
          <>
            <p>Ingresa los datos para conectar tu correo electrónico.</p>
            
            <div>
              <label>Correo Electrónico</label>
              <input 
                type="email" 
                placeholder="ejemplo@correo.com" 
                value={email}
                onChange={e => setEmail(e.target.value)}
              />
            </div>
            
            <div>
              <label>Contraseña / App Password</label>
              <input 
                type="password" 
                value={password}
                onChange={e => setPassword(e.target.value)}
              />
            </div>
            
            <div className="modal-actions">
              <button className="btn" onClick={onClose}>Cancelar</button>
              <button 
                className="btn primary" 
                style={{ width: 'auto' }}
                onClick={handleConnect}
              >
                Conectar
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default EmailModal;
