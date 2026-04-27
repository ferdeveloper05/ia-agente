import React, { useState } from 'react';

const SettingsModal = ({ onClose, onDeleteAllChats }) => {
  const [activeTab, setActiveTab] = useState('general');

  const tabs = [
    { id: 'general', label: 'General', icon: '⚙️' },
    { id: 'chats', label: 'Chats', icon: '💬' },
    { id: 'account', label: 'Account', icon: '👤' },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'general':
        return (
          <div className="settings-section">
            <h2 className="settings-section-title">General Settings</h2>
            <div className="settings-field">
              <label>Theme</label>
              <select className="settings-select">
                <option value="system">System</option>
                <option value="dark">Dark</option>
                <option value="light">Light</option>
              </select>
            </div>
            <div className="settings-field">
              <label>Language</label>
              <select className="settings-select">
                <option value="es">Español</option>
                <option value="en">English</option>
                <option value="pt">Português</option>
              </select>
            </div>
          </div>
        );
      case 'chats':
        return (
          <div className="settings-section">
            <h2 className="settings-section-title">Chat Management</h2>
            <div className="settings-action-list">
              <button className="btn settings-action-btn">📥 Importar chats</button>
              <button className="btn settings-action-btn">📤 Exportar chats</button>
              <button 
                className="btn settings-action-btn danger" 
                onClick={() => {
                  if (window.confirm('¿Estás seguro de que deseas eliminar TODOS los chats?')) {
                    onDeleteAllChats();
                    onClose();
                  }
                }}
              >
                🗑️ Eliminar todos los chats
              </button>
            </div>
          </div>
        );
      case 'account':
        return (
          <div className="settings-section">
            <h2 className="settings-section-title">Account Settings</h2>
            <div className="settings-action-list">
              <button className="btn settings-action-btn" onClick={() => alert('Próximamente...')}>✏️ Editar cuenta</button>
              <button className="btn settings-action-btn" onClick={() => alert('Próximamente...')}>🔑 Restablecer contraseña</button>
              <button className="btn settings-action-btn" onClick={() => alert('Próximamente...')}>🔄 Cambiar contraseña</button>
              <button 
                className="btn settings-action-btn danger"
                onClick={() => alert('Esta acción es irreversible. Próximamente...')}
              >
                🚫 Eliminar cuenta
              </button>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content settings-modal" onClick={(e) => e.stopPropagation()}>
        <div className="settings-sidebar">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              className={`settings-sidebar-item ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <span style={{ marginRight: '0.75rem' }}>{tab.icon}</span>
              {tab.label}
            </button>
          ))}
          <div style={{ flexGrow: 1 }} />
          <button className="btn" onClick={onClose}>Cerrar</button>
        </div>
        <div className="settings-content">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default SettingsModal;
