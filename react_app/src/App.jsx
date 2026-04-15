import { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import EmailModal from './components/EmailModal'

function App() {
  const [conversations, setConversations] = useState({})
  const [currentConversationId, setCurrentConversationId] = useState(null)
  const [isEmailModalOpen, setIsEmailModalOpen] = useState(false)
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false)

  // Initialize first conversation
  useEffect(() => {
    if (Object.keys(conversations).length === 0) {
      createNewConversation()
    }
  }, [])

  const generateId = () => Math.random().toString(36).substr(2, 9)

  const createNewConversation = () => {
    // Check if there is an empty conversation already
    const emptyConvId = Object.keys(conversations).find(
      id => conversations[id].messages.length === 0
    );

    if (emptyConvId) {
      setCurrentConversationId(emptyConvId);
      return;
    }

    const newId = generateId()
    setConversations(prev => ({
      ...prev,
      [newId]: {
        title: 'Nueva conversación',
        messages: []
      }
    }))
    setCurrentConversationId(newId)
  }

  const switchConversation = (id) => {
    setCurrentConversationId(id)
  }

  const deleteConversation = (id) => {
    const newConvs = { ...conversations }
    delete newConvs[id]
    setConversations(newConvs)

    if (currentConversationId === id) {
      const remainingIds = Object.keys(newConvs)
      if (remainingIds.length > 0) {
        setCurrentConversationId(remainingIds[0])
      } else {
        createNewConversation()
      }
    }
  }

  const renameConversation = (id, newTitle) => {
    setConversations(prev => ({
      ...prev,
      [id]: {
        ...prev[id],
        title: newTitle || 'Conversación'
      }
    }))
  }

  const addMessage = (content, role = 'user') => {
    if (!currentConversationId) return;

    setConversations(prev => {
      const conv = prev[currentConversationId]
      const newMessages = [...conv.messages, { role, content }]
      
      // Update title on first user message
      let newTitle = conv.title
      // Solo cambiar titulo automaticamente si es el primer mensaje y el titulo aun era el default
      if (role === 'user' && conv.messages.length === 0 && conv.title === 'Nueva conversación') {
        newTitle = content.length > 20 ? content.substring(0, 20) + '...' : content
      }

      return {
        ...prev,
        [currentConversationId]: {
          ...conv,
          title: newTitle,
          messages: newMessages
        }
      }
    })
  }

  return (
    <div className="app-container">
      <Sidebar 
        conversations={conversations}
        currentConversationId={currentConversationId}
        createNewConversation={createNewConversation}
        switchConversation={switchConversation}
        deleteConversation={deleteConversation}
        renameConversation={renameConversation}
        openEmailModal={() => setIsEmailModalOpen(true)}
        isCollapsed={isSidebarCollapsed}
        toggleSidebar={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
      />
      <ChatArea 
        currentConversation={conversations[currentConversationId]}
        addMessage={addMessage}
        toggleSidebar={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
        isSidebarCollapsed={isSidebarCollapsed}
      />
      {isEmailModalOpen && (
        <EmailModal onClose={() => setIsEmailModalOpen(false)} />
      )}
    </div>
  )
}

export default App
