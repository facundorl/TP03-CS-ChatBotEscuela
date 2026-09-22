import { useState, useRef, useEffect, Fragment } from 'react'
import { Bot, User, Send, AlertCircle } from 'lucide-react'
import './App.css'

const API_URL = 'http://localhost:5000/chat'

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'bot',
      text: 'Hola. Soy el asistente de la Escuela Técnica N° 36 D.E. 15. ¿En qué consulta escolar te puedo ayudar?',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      sugerencias: [
        { tag: 'especialidades', titulo: 'Especialidades', consulta: 'qué especialidades tiene la escuela' },
        { tag: 'inscripciones', titulo: 'Inscripciones', consulta: 'cómo me anoto a la escuela' },
        { tag: 'horarios', titulo: 'Horarios', consulta: 'cuales son los horarios' }
      ]
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, loading])

  
  const handleSend = async (e, textoDirecto = null) => {
    if (e) e.preventDefault()
    const query = (textoDirecto ?? input).trim()
    if (!query || loading) return

    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      text: query,
      time: now
    }

    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: query })
      })

      if (!response.ok) {
        throw new Error(`Error ${response.status}`)
      }

      const data = await response.json()
      const botMsg = {
        id: Date.now() + 1,
        sender: 'bot',
        text: data.response || 'Sin respuesta del servidor.',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        sugerencias: Array.isArray(data.sugerencias) ? data.sugerencias : []
      }

      setMessages((prev) => [...prev, botMsg])
    } catch (err) {
      console.error('Error de conexión:', err)
      const errorMsg = {
        id: Date.now() + 1,
        sender: 'bot',
        isError: true,
        text: 'No se pudo conectar con el servidor en el puerto 5000.',
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }
      setMessages((prev) => [...prev, errorMsg])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chat-container">
      <header className="chat-header">
        <h1>Escuela Técnica N° 36 D.E. 15</h1>
      </header>

      <main className="messages-area">
        {messages.map((msg, index) => {
        const esUltimoMensaje = index === messages.length - 1
        const mostrarSugerencias =
          msg.sender === 'bot' &&
          !msg.isError &&
          esUltimoMensaje &&
          !loading &&
          Array.isArray(msg.sugerencias) &&
          msg.sugerencias.length > 0

        return (
          <Fragment key={msg.id}>
          <div
            className={`message-row ${msg.sender === 'user' ? 'row-user' : 'row-bot'}`}
          >
            {msg.sender === 'bot' && (
              <div className={`avatar ${msg.isError ? 'avatar-error' : ''}`}>
                {msg.isError ? <AlertCircle size={15} /> : <Bot size={15} />}
              </div>
            )}

            <div className={`bubble ${msg.sender === 'user' ? 'bubble-user' : 'bubble-bot'} ${msg.isError ? 'bubble-error' : ''}`}>
              <div className="bubble-text">{msg.text}</div>
              <div className="bubble-time">{msg.time}</div>
            </div>

            {msg.sender === 'user' && (
              <div className="avatar avatar-user">
                <User size={15} />
              </div>
            )}
          </div>

          {mostrarSugerencias && (
            <div className="sugerencias-row">
              <span className="sugerencias-label">Temas relacionados</span>
              <div className="sugerencias-chips">
                {msg.sugerencias.map((s) => (
                  <button
                    key={s.tag}
                    type="button"
                    className="chip-sugerencia"
                    onClick={() => handleSend(null, s.consulta)}
                    disabled={loading}
                  >
                    {s.titulo}
                  </button>
                ))}
              </div>
            </div>
          )}
          </Fragment>
        )
        })}

        {loading && (
          <div className="message-row row-bot">
            <div className="avatar">
              <Bot size={15} />
            </div>
            <div className="bubble bubble-bot typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      <form className="input-area" onSubmit={handleSend}>
        <input
          type="text"
          placeholder="Escribí tu consulta..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          autoFocus
        />
        <button type="submit" disabled={!input.trim() || loading} aria-label="Enviar">
          <Send size={16} />
        </button>
      </form>
    </div>
  )
}

export default App
