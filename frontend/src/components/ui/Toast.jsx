import { useState, useEffect } from 'react'

export const Toast = ({ message, type = 'success', duration = 3000, onClose }) => {
  const [isVisible, setIsVisible] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false)
      setTimeout(onClose, 300) // Wait for animation
    }, duration)
    return () => clearTimeout(timer)
  }, [duration, onClose])

  const getStyles = () => {
    const base = "fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg border flex items-center space-x-3 transform transition-all duration-300"
    const variants = {
      success: "bg-emerald-50 border-emerald-200 text-emerald-800",
      error: "bg-red-50 border-red-200 text-red-800",
      info: "bg-blue-50 border-blue-200 text-blue-800"
    }
    return `${base} ${variants[type]} ${isVisible ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'}`
  }

  const getIcon = () => {
    const icons = {
      success: '✅',
      error: '❌',
      info: 'ℹ️'
    }
    return icons[type]
  }

  return (
    <div className={getStyles()}>
      <span className="text-lg">{getIcon()}</span>
      <span className="font-medium">{message}</span>
      <button 
        onClick={() => setIsVisible(false)}
        className="ml-2 text-gray-400 hover:text-gray-600 transition-colors"
      >
        ✕
      </button>
    </div>
  )
}

export const useToast = () => {
  const [toasts, setToasts] = useState([])

  const showToast = (message, type = 'success') => {
    const id = Date.now()
    setToasts(prev => [...prev, { id, message, type }])
  }

  const removeToast = (id) => {
    setToasts(prev => prev.filter(toast => toast.id !== id))
  }

  const ToastContainer = () => (
    <>
      {toasts.map(toast => (
        <Toast
          key={toast.id}
          message={toast.message}
          type={toast.type}
          onClose={() => removeToast(toast.id)}
        />
      ))}
    </>
  )

  return { showToast, ToastContainer }
}