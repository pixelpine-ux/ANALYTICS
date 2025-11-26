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
    <nav className="bg-white/95 backdrop-blur-md shadow-soft border-b border-slate-200/60 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center space-x-8">
            <Link to="/" className="flex items-center space-x-3 group">
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-lg group-hover:scale-105 transition-transform duration-200">
                <span className="text-white font-bold text-lg">📈</span>
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
                Analytics
              </span>
            </Link>
            <div className="flex bg-slate-100/80 backdrop-blur-sm rounded-xl p-1.5 border border-slate-200/50">
              <Link
                to="/"
                className={`px-5 py-2.5 rounded-lg text-sm font-medium transition-all duration-300 flex items-center space-x-2 ${
                  isActive('/')
                    ? 'bg-white text-primary-600 shadow-md border border-primary-100 transform scale-105'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/70 hover:scale-102'
                }`}
              >
                <span className="text-base">📈</span>
                <span>Dashboard</span>
              </Link>
              <Link
                to="/upload"
                className={`px-5 py-2.5 rounded-lg text-sm font-medium transition-all duration-300 flex items-center space-x-2 ${
                  isActive('/upload')
                    ? 'bg-white text-primary-600 shadow-md border border-primary-100 transform scale-105'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/70 hover:scale-102'
                }`}
              >
                <span className="text-base">📄</span>
                <span>Upload</span>
              </Link>
            </div>
          </div>
          
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2 text-sm text-slate-500 bg-slate-50 px-3 py-1.5 rounded-full border border-slate-200">
              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></div>
              <span className="font-medium">Live Data</span>
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
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <Navigation />
        <main className="animate-fade-in">
          <Routes>
            <Route path="/" element={<SimpleDashboard />} />
            <Route path="/debug" element={<div className="p-8"><DebugAPI /></div>} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/test" element={<TestDashboard />} />
            <Route path="/upload" element={<Upload />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App