# Frontend Quick Start Guide
## Get Your React Dashboard Running in 30 Minutes

### 🚀 Phase 1: Project Setup (10 minutes)

#### **1. Initialize React Project**
```bash
cd /home/dog/Desktop/ANALYTICS/frontend
npm create vite@latest . -- --template react
npm install

# Install core dependencies
npm install @tanstack/react-query react-router-dom
npm install chart.js react-chartjs-2
npm install react-hook-form @hookform/resolvers yup
npm install clsx tailwind-merge

# Install dev dependencies
npm install -D tailwindcss postcss autoprefixer
npm install -D @testing-library/react @testing-library/jest-dom
npx tailwindcss init -p
```

#### **2. Configure Tailwind CSS**
```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8'
        }
      }
    },
  },
  plugins: [],
}
```

#### **3. Basic Project Structure**
```bash
mkdir -p src/{components,pages,services,hooks,utils}
mkdir -p src/components/{ui,charts,forms}
```

---

### 📊 Phase 2: Core Components (10 minutes)

#### **1. API Client Setup**
```javascript
// src/services/api.js
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const apiClient = {
  async get(endpoint, params = {}) {
    const url = new URL(`${API_BASE}${endpoint}`)
    Object.keys(params).forEach(key => 
      url.searchParams.append(key, params[key])
    )
    
    const response = await fetch(url)
    if (!response.ok) throw new Error(`API Error: ${response.status}`)
    return response.json()
  },

  async post(endpoint, data) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    if (!response.ok) throw new Error(`API Error: ${response.status}`)
    return response.json()
  }
}
```

#### **2. KPI Card Component**
```javascript
// src/components/ui/KPICard.jsx
export const KPICard = ({ title, value, format = 'number', loading = false }) => {
  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
        <div className="h-8 bg-gray-200 rounded w-3/4"></div>
      </div>
    )
  }

  const formatValue = (val) => {
    if (format === 'currency') return `$${val.toLocaleString()}`
    if (format === 'percentage') return `${val}%`
    return val.toLocaleString()
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <dt className="text-sm font-medium text-gray-500">{title}</dt>
      <dd className="mt-1 text-3xl font-semibold text-gray-900">
        {formatValue(value)}
      </dd>
    </div>
  )
}
```

#### **3. Basic Dashboard Layout**
```javascript
// src/pages/Dashboard.jsx
import { useState, useEffect } from 'react'
import { KPICard } from '../components/ui/KPICard'
import { apiClient } from '../services/api'

export const Dashboard = () => {
  const [kpis, setKpis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchKPIs = async () => {
      try {
        const data = await apiClient.get('/kpis/summary', { days_back: 30 })
        setKpis(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchKPIs()
  }, [])

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Unable to load dashboard
          </h2>
          <p className="text-gray-600">{error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Your business insights for the last 30 days
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <KPICard
            title="Total Revenue"
            value={kpis?.total_revenue || 0}
            format="currency"
            loading={loading}
          />
          <KPICard
            title="Total Sales"
            value={kpis?.total_sales_count || 0}
            loading={loading}
          />
          <KPICard
            title="Average Order"
            value={kpis?.average_order_value || 0}
            format="currency"
            loading={loading}
          />
          <KPICard
            title="Repeat Customers"
            value={kpis?.repeat_customers_count || 0}
            loading={loading}
          />
        </div>

        {kpis?.top_products && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Top Products
            </h2>
            <div className="space-y-3">
              {kpis.top_products.slice(0, 5).map((product, index) => (
                <div key={product.product_name} className="flex justify-between items-center">
                  <span className="font-medium">
                    {index + 1}. {product.product_name}
                  </span>
                  <span className="text-gray-600">
                    ${product.total_revenue.toLocaleString()} ({product.sales_count} sales)
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
```

---

### 📤 Phase 3: Upload Interface (10 minutes)

#### **1. File Upload Component**
```javascript
// src/components/forms/FileUpload.jsx
import { useState, useCallback } from 'react'
import { apiClient } from '../../services/api'

export const FileUpload = ({ onSuccess }) => {
  const [dragActive, setDragActive] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState(null)

  const uploadFile = async (file) => {
    setUploading(true)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('http://localhost:8000/api/v1/upload/csv', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) throw new Error('Upload failed')
      
      const data = await response.json()
      setResult(data)
      onSuccess?.(data)
    } catch (error) {
      setResult({ error: error.message })
    } finally {
      setUploading(false)
    }
  }

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setDragActive(false)
    
    const files = Array.from(e.dataTransfer.files)
    const csvFile = files.find(file => file.name.endsWith('.csv'))
    
    if (csvFile) {
      uploadFile(csvFile)
    } else {
      setResult({ error: 'Please upload a CSV file' })
    }
  }, [])

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) uploadFile(file)
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div
        className={`
          border-2 border-dashed rounded-lg p-8 text-center transition-colors
          ${dragActive ? 'border-blue-400 bg-blue-50' : 'border-gray-300'}
          ${uploading ? 'opacity-50 pointer-events-none' : 'cursor-pointer hover:border-gray-400'}
        `}
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        onDragEnter={() => setDragActive(true)}
        onDragLeave={() => setDragActive(false)}
        onClick={() => document.getElementById('file-input').click()}
      >
        <input
          id="file-input"
          type="file"
          accept=".csv"
          onChange={handleFileSelect}
          className="hidden"
        />
        
        {uploading ? (
          <div>
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Uploading and processing...</p>
          </div>
        ) : (
          <div>
            <div className="text-4xl mb-4">📊</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Upload your sales data
            </h3>
            <p className="text-gray-600 mb-4">
              Drag and drop your CSV file here, or click to select
            </p>
            <p className="text-sm text-gray-500">
              Required columns: date, product_name, amount
            </p>
          </div>
        )}
      </div>

      {result && (
        <div className={`mt-6 p-4 rounded-lg ${
          result.error ? 'bg-red-50 border border-red-200' : 'bg-green-50 border border-green-200'
        }`}>
          {result.error ? (
            <div>
              <h4 className="font-medium text-red-800">Upload Failed</h4>
              <p className="text-red-700">{result.error}</p>
            </div>
          ) : (
            <div>
              <h4 className="font-medium text-green-800">Upload Successful!</h4>
              <p className="text-green-700">
                Processed {result.records_processed} records
              </p>
              {result.errors?.length > 0 && (
                <details className="mt-2">
                  <summary className="cursor-pointer text-sm">
                    {result.errors.length} warnings
                  </summary>
                  <ul className="mt-2 text-sm space-y-1">
                    {result.errors.map((error, i) => (
                      <li key={i} className="text-red-600">• {error}</li>
                    ))}
                  </ul>
                </details>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
```

#### **2. Upload Page**
```javascript
// src/pages/Upload.jsx
import { useState } from 'react'
import { FileUpload } from '../components/forms/FileUpload'

export const Upload = () => {
  const [uploadSuccess, setUploadSuccess] = useState(false)

  const handleUploadSuccess = (result) => {
    setUploadSuccess(true)
    // Optionally redirect to dashboard after delay
    setTimeout(() => {
      window.location.href = '/'
    }, 2000)
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Upload Sales Data</h1>
          <p className="mt-2 text-gray-600">
            Import your sales data to generate analytics insights
          </p>
        </div>

        <FileUpload onSuccess={handleUploadSuccess} />

        {uploadSuccess && (
          <div className="mt-8 text-center">
            <div className="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-lg">
              <span className="mr-2">✅</span>
              Data uploaded successfully! Redirecting to dashboard...
            </div>
          </div>
        )}

        <div className="mt-12 bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">CSV Format Requirements</h2>
          <div className="bg-gray-50 p-4 rounded font-mono text-sm">
            <div className="font-semibold mb-2">Required columns:</div>
            <div>date,product_name,amount</div>
            <div className="mt-2 font-semibold">Optional columns:</div>
            <div>customer_id,category</div>
            <div className="mt-4 font-semibold">Example:</div>
            <div>2024-01-15,Coffee,5.99,CUST001,beverages</div>
            <div>2024-01-16,Sandwich,8.50,CUST002,food</div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

---

### 🔗 Phase 4: App Integration

#### **1. Main App Component**
```javascript
// src/App.jsx
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import { Dashboard } from './pages/Dashboard'
import { Upload } from './pages/Upload'
import './App.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center space-x-8">
                <Link to="/" className="text-xl font-bold text-gray-900">
                  Analytics Dashboard
                </Link>
                <div className="flex space-x-4">
                  <Link 
                    to="/" 
                    className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md"
                  >
                    Dashboard
                  </Link>
                  <Link 
                    to="/upload" 
                    className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md"
                  >
                    Upload Data
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
```

#### **2. Environment Configuration**
```bash
# .env
VITE_API_URL=http://localhost:8000/api/v1
```

#### **3. CSS Setup**
```css
/* src/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

---

### 🚀 Launch Commands

```bash
# Start frontend development server
npm run dev

# Start backend (in separate terminal)
cd ../backend
python3 run_dev.py

# Your app will be available at:
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

### ✅ Testing Your Setup

1. **Start both servers** (frontend + backend)
2. **Visit http://localhost:5173** - Should see dashboard
3. **Click "Upload Data"** - Should see upload interface
4. **Upload a CSV file** - Should process and redirect to dashboard
5. **Check dashboard** - Should show your uploaded data

### 🎯 What You've Built

- ✅ **Responsive Dashboard** with KPI cards
- ✅ **File Upload Interface** with drag & drop
- ✅ **Error Handling** for failed uploads
- ✅ **Navigation** between pages
- ✅ **API Integration** with your FastAPI backend
- ✅ **Professional UI** with Tailwind CSS

### 🚀 Next Steps

From here you can:
1. **Add Charts** using Chart.js
2. **Implement React Query** for better data management
3. **Add Admin Panel** for settings
4. **Create PDF Export** functionality
5. **Add Authentication** and user management

**You now have a working full-stack analytics application!** 🎉