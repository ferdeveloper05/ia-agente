import React, { useState, useEffect, useRef } from 'react';

// SVG Icons
const PanelLeftIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/>
  </svg>
);

const PlusIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M5 12h14"/><path d="M12 5v14"/>
  </svg>
);

const SearchIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>
  </svg>
);

const KebabIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="1"/><circle cx="12" cy="5" r="1"/><circle cx="12" cy="19" r="1"/>
  </svg>
);

function Sidebar({ 
  conversations, 
  currentConversationId, 
  createNewConversation, 
  switchConversation, 
  deleteConversation,
  renameConversation,
  openEmailModal,
  isCollapsed,
  toggleSidebar
}) {
  const [openMenuId, setOpenMenuId] = useState(null);
  const [modalState, setModalState] = useState(null); // null, {type: 'rename', id}, {type: 'delete', id}
  const [renameInput, setRenameInput] = useState('');
  const dropdownRef = useRef(null);

  const sortedConvIds = Object.keys(conversations).reverse();

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setOpenMenuId(null);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleRenameClick = (id, currentTitle) => {
    setOpenMenuId(null);
    setRenameInput(currentTitle);
    setModalState({ type: 'rename', id });
  };

  const handleDeleteClick = (id) => {
    setOpenMenuId(null);
    setModalState({ type: 'delete', id });
  };

  const submitRename = () => {
    if (renameInput.trim() !== '') {
      renameConversation(modalState.id, renameInput.trim());
    }
    setModalState(null);
  };

  const submitDelete = () => {
    deleteConversation(modalState.id);
    setModalState(null);
  };

  if (isCollapsed) {
    return (
      <div className="sidebar collapsed">
        <div className="sidebar-top-icons">
          <button className="icon-btn" onClick={toggleSidebar} title="Expandir Panel">
            <PanelLeftIcon />
          </button>
          <button className="icon-btn" onClick={createNewConversation} title="Nueva Conversación">
            <PlusIcon />
          </button>
          <button className="icon-btn" title="Buscar">
            <SearchIcon />
          </button>
        </div>
        <div className="sidebar-bottom-icons">
          <button className="icon-profile-btn" onClick={openEmailModal} title="Perfil / Email">
            F
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <button className="icon-btn toggle-btn" onClick={toggleSidebar} title="Ocultar Panel">
          <PanelLeftIcon />
        </button>
      </div>

      <div className="sidebar-title">
        🤖 Chatbot AI
      </div>
      
      <button className="btn primary" onClick={createNewConversation}>
        ➕ Nueva conversación
      </button>

      <hr />
      <h3 style={{ marginBottom: '1rem', fontSize: '0.9rem', fontWeight: 500 }}>Conversaciones</h3>
      
      <div className="conv-list">
        {sortedConvIds.map(id => {
          const conv = conversations[id];
          const isActive = id === currentConversationId;
          const isMenuOpen = openMenuId === id;

          return (
            <div key={id} className={`conv-item ${isActive ? 'active' : ''}`}>
              <button 
                className="btn" 
                onClick={() => switchConversation(id)}
                style={{ flexGrow: 1 }}
              >
                💬 {conv.title}
              </button>
              
              <div className="kebab-container" ref={isMenuOpen ? dropdownRef : null}>
                <button 
                  className="btn btn-kebab" 
                  onClick={(e) => {
                    e.stopPropagation();
                    setOpenMenuId(isMenuOpen ? null : id);
                  }}
                  title="Opciones"
                >
                  <KebabIcon />
                </button>
                
                {isMenuOpen && (
                  <div className="dropdown-menu">
                    <button onClick={() => handleRenameClick(id, conv.title)}>✏️ Editar titulo</button>
                    <button className="delete-opt" onClick={() => handleDeleteClick(id)}>🗑️ Eliminar chat</button>
                  </div>
                )}
              </div>
            </div>
          )
        })}
      </div>

      <hr />

      <button className="btn" onClick={openEmailModal}>
        📧 Conectar Correo
      </button>

      {/* --- Custom Modals --- */}
      {modalState?.type === 'rename' && (
        <div className="modal-overlay" onClick={() => setModalState(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h3>Editar título</h3>
            <p style={{ marginBottom: '0.5rem' }}>Ingresa el nuevo nombre para la conversación:</p>
            <input 
              type="text" 
              value={renameInput}
              onChange={e => setRenameInput(e.target.value)}
              autoFocus
              onKeyDown={(e) => {
                if (e.key === 'Enter') submitRename();
                if (e.key === 'Escape') setModalState(null);
              }}
            />
            <div className="modal-actions">
              <button className="btn" onClick={() => setModalState(null)}>Cancelar</button>
              <button className="btn primary" onClick={submitRename} style={{ width: 'auto' }}>Guardar</button>
            </div>
          </div>
        </div>
      )}

      {modalState?.type === 'delete' && (
        <div className="modal-overlay" onClick={() => setModalState(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h3>Eliminar conversación</h3>
            <p style={{ marginBottom: '1rem' }}>
              ¿Estás seguro de que deseas eliminar esta conversación? Esta acción no se puede deshacer.
            </p>
            <div className="modal-actions">
              <button className="btn" onClick={() => setModalState(null)}>Cancelar</button>
              <button 
                className="btn primary" 
                onClick={submitDelete} 
                style={{ width: 'auto', backgroundColor: '#ef4444', borderColor: '#ef4444' }}
              >
                Eliminar
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

export default Sidebar;
