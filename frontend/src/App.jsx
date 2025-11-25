import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import { Dashboard } from './pages/Dashboard'
import { Upload } from './pages/Upload'
import { TestDashboard } from './pages/TestDashboard'
import { SimpleDashboard } from './pages/SimpleDashboard'
import { DebugAPI } from './components/DebugAPI'
import './index.css'

const Navigation = () => {
  const location = useLocation()
  
  const isActive = (path) => location.pathname === path

  return (
    <nav className="bg-white/95 backdrop-blur-md shadow-soft border-b border-slate-200/60">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center space-x-8">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">📈</span>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
                Analytics
              </span>
            </Link>
            <div className="flex bg-slate-100 rounded-lg p-1">
              <Link
                to="/"
                className={`px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 flex items-center space-x-2 ${
                  isActive('/')
                    ? 'bg-white text-primary-600 shadow-sm'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                }`}
              >
                <span>📈</span>
                <span>Dashboard</span>
              </Link>
              <Link
                to="/upload"
                className={`px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 flex items-center space-x-2 ${
                  isActive('/upload')
                    ? 'bg-white text-primary-600 shadow-sm'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                }`}
              >
                <span>📄</span>
                <span>Upload</span>
              </Link>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-sm text-slate-500">
              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
              <span>Live Data</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <Routes>
          <Route path="/" element={<SimpleDashboard />} />
          <Route path="/debug" element={<div className="p-8"><DebugAPI /></div>} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/test" element={<TestDashboard />} />
          <Route path="/upload" element={<Upload />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App