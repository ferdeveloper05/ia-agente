import React, { useState } from 'react';

function EmailModal({ onClose, onConnected }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const validateEmail = (email) => {
    // Regex estricto: usuario@dominio.extension (min 2 chars en extensión)
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(email);
  };

  const validate = () => {
    const newErrors = {};

    if (!name.trim()) {
      newErrors.name = 'El nombre es obligatorio.';
    } else if (name.trim().length < 2) {
      newErrors.name = 'El nombre debe tener al menos 2 caracteres.';
    }

    if (!email.trim()) {
      newErrors.email = 'El correo es obligatorio.';
    } else if (!validateEmail(email)) {
      newErrors.email = 'Ingresa un correo electrónico válido (ej: usuario@dominio.com).';
    }

    if (!password.trim()) {
      newErrors.password = 'La contraseña es obligatoria.';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleConnect = async () => {
    if (!validate()) return;

    setIsLoading(true);
    setErrors({});

    try {
      // Verificar el formato del email en el backend
      const res = await fetch('http://localhost:8000/api/v1/validate-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, name: name.trim() })
      });

      const data = await res.json();

      if (!res.ok || !data.valid) {
        setErrors({ email: data.detail || 'El correo no pudo ser verificado.' });
        setIsLoading(false);
        return;
      }

      setSuccess(true);
      if (onConnected) onConnected(name.trim());
      setTimeout(() => {
        onClose();
      }, 1500);
    } catch (err) {
      setErrors({ general: 'No se pudo conectar con el servidor.' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <h3>Conectar Correo Electrónico</h3>
        
        {success ? (
          <div style={{ color: '#00cc66', padding: '1rem 0' }}>
            ✅ Correo <strong>{email}</strong> conectado correctamente.
          </div>
        ) : (
          <>
            <p style={{ marginBottom: '0.5rem', color: '#94A3B8', fontSize: '0.9rem' }}>
              Ingresa tus datos para vincular tu correo electrónico.
            </p>

            {errors.general && (
              <div style={{ color: '#FF4B4B', fontSize: '0.85rem', marginBottom: '0.5rem' }}>
                {errors.general}
              </div>
            )}
            
            <div>
              <label>Nombre</label>
              <input 
                type="text" 
                placeholder="Tu nombre completo" 
                value={name}
                onChange={e => setName(e.target.value)}
                style={errors.name ? { borderColor: '#FF4B4B' } : {}}
              />
              {errors.name && (
                <span style={{ color: '#FF4B4B', fontSize: '0.8rem', display: 'block', marginTop: '-0.5rem', marginBottom: '0.5rem' }}>
                  {errors.name}
                </span>
              )}
            </div>

            <div>
              <label>Correo Electrónico</label>
              <input 
                type="email" 
                placeholder="ejemplo@correo.com" 
                value={email}
                onChange={e => setEmail(e.target.value)}
                style={errors.email ? { borderColor: '#FF4B4B' } : {}}
              />
              {errors.email && (
                <span style={{ color: '#FF4B4B', fontSize: '0.8rem', display: 'block', marginTop: '-0.5rem', marginBottom: '0.5rem' }}>
                  {errors.email}
                </span>
              )}
            </div>
            
            <div>
              <label>Contraseña / App Password</label>
              <input 
                type="password" 
                value={password}
                onChange={e => setPassword(e.target.value)}
                style={errors.password ? { borderColor: '#FF4B4B' } : {}}
              />
              {errors.password && (
                <span style={{ color: '#FF4B4B', fontSize: '0.8rem', display: 'block', marginTop: '-0.5rem', marginBottom: '0.5rem' }}>
                  {errors.password}
                </span>
              )}
            </div>
            
            <div className="modal-actions">
              <button className="btn" onClick={onClose} disabled={isLoading}>Cancelar</button>
              <button 
                className="btn primary" 
                style={{ width: 'auto' }}
                onClick={handleConnect}
                disabled={isLoading}
              >
                {isLoading ? 'Verificando...' : 'Conectar'}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default EmailModal;
