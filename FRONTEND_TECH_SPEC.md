# Frontend Technical Specification
## React Analytics Dashboard - Implementation Details

### 🏗️ Architecture Overview

**Frontend Architecture Pattern: Component-Based with Service Layer**
```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
├─────────────────────────────────────────────────────────┤
│  Pages Layer    │ Dashboard │ Upload │ Admin │ Reports  │
├─────────────────────────────────────────────────────────┤
│ Components Layer│ KPICard │ Charts │ Forms │ Tables    │
├─────────────────────────────────────────────────────────┤
│  Hooks Layer    │ useAnalytics │ useUpload │ useAuth   │
├─────────────────────────────────────────────────────────┤
│ Services Layer  │ API Client │ Formatters │ Validators │
├─────────────────────────────────────────────────────────┤
│  Backend API    │ FastAPI Server (Port 8000)           │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Component Specifications

### **1. Core Layout Components**

#### **AppLayout.jsx**
```javascript
// Purpose: Main application shell with navigation
// Props: { children, currentPage }
// Features: Responsive sidebar, header, breadcrumbs

const AppLayout = ({ children, currentPage }) => (
  <div className="min-h-screen bg-gray-50">
    <Sidebar currentPage={currentPage} />
    <div className="lg:pl-64">
      <Header />
      <main className="py-6">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          {children}
        </div>
      </main>
    </div>
  </div>
)
```

#### **KPICard.jsx**
```javascript
// Purpose: Display single metric with trend indicator
// Props: { title, value, change, format, loading }
// Features: Loading skeleton, trend arrows, color coding

const KPICard = ({ title, value, change, format = 'currency' }) => {
  const formattedValue = formatters[format](value)
  const trendColor = change >= 0 ? 'text-green-600' : 'text-red-600'
  
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <dt className="text-sm font-medium text-gray-500 truncate">
              {title}
            </dt>
            <dd className="mt-1 text-3xl font-semibold text-gray-900">
              {formattedValue}
            </dd>
          </div>
          {change !== undefined && (
            <div className={`ml-auto ${trendColor}`}>
              <TrendIcon change={change} />
              <span className="text-sm font-medium">
                {Math.abs(change)}%
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
```

### **2. Chart Components**

#### **RevenueChart.jsx**
```javascript
// Purpose: Line chart showing revenue trends over time
// Props: { data, timeframe, height }
// Features: Responsive, interactive tooltips, zoom

import { Line } from 'react-chartjs-2'

const RevenueChart = ({ data, timeframe = 'daily' }) => {
  const chartData = {
    labels: data.map(item => formatDate(item.period, timeframe)),
    datasets: [{
      label: 'Revenue',
      data: data.map(item => item.revenue),
      borderColor: '#2563eb',
      backgroundColor: 'rgba(37, 99, 235, 0.1)',
      fill: true,
      tension: 0.4
    }]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: (value) => formatCurrency(value)
        }
      }
    },
    plugins: {
      tooltip: {
        callbacks: {
          label: (context) => `Revenue: ${formatCurrency(context.parsed.y)}`
        }
      }
    }
  }

  return (
    <div className="h-64 sm:h-80">
      <Line data={chartData} options={options} />
    </div>
  )
}
```

#### **TopProductsChart.jsx**
```javascript
// Purpose: Horizontal bar chart for top products
// Props: { products, maxItems }
// Features: Color-coded bars, click to drill down

const TopProductsChart = ({ products, maxItems = 5 }) => {
  const chartData = {
    labels: products.slice(0, maxItems).map(p => p.product_name),
    datasets: [{
      label: 'Revenue',
      data: products.slice(0, maxItems).map(p => p.total_revenue),
      backgroundColor: [
        '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'
      ]
    }]
  }

  return <Bar data={chartData} options={horizontalBarOptions} />
}
```

### **3. Upload Components**

#### **FileUpload.jsx**
```javascript
// Purpose: Drag & drop file upload with validation
// Props: { onUpload, acceptedTypes, maxSize }
// Features: Progress tracking, error display, preview

const FileUpload = ({ onUpload, maxSize = 10 * 1024 * 1024 }) => {
  const [dragActive, setDragActive] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setDragActive(false)
    
    const files = Array.from(e.dataTransfer.files)
    const csvFile = files.find(file => file.type === 'text/csv')
    
    if (!csvFile) {
      showError('Please upload a CSV file')
      return
    }
    
    if (csvFile.size > maxSize) {
      showError('File too large. Maximum size is 10MB')
      return
    }
    
    uploadFile(csvFile)
  }, [maxSize])

  return (
    <div
      className={`
        border-2 border-dashed rounded-lg p-6 text-center
        ${dragActive ? 'border-blue-400 bg-blue-50' : 'border-gray-300'}
        ${uploading ? 'pointer-events-none opacity-50' : 'cursor-pointer'}
      `}
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      onDragEnter={() => setDragActive(true)}
      onDragLeave={() => setDragActive(false)}
    >
      {uploading ? (
        <UploadProgress progress={progress} />
      ) : (
        <UploadPrompt />
      )}
    </div>
  )
}
```

---

## 🔌 API Integration Layer

### **API Client Setup**
```javascript
// services/api.js
class APIClient {
  constructor(baseURL = process.env.REACT_APP_API_URL) {
    this.baseURL = baseURL
    this.defaultHeaders = {
      'Content-Type': 'application/json'
    }
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const config = {
      headers: { ...this.defaultHeaders, ...options.headers },
      ...options
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        throw new APIError(response.status, await response.json())
      }
      
      return await response.json()
    } catch (error) {
      if (error instanceof APIError) throw error
      throw new NetworkError('Network request failed')
    }
  }

  // Convenience methods
  get(endpoint, params = {}) {
    const query = new URLSearchParams(params).toString()
    return this.request(`${endpoint}${query ? `?${query}` : ''}`)
  }

  post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  upload(endpoint, file, onProgress) {
    const formData = new FormData()
    formData.append('file', file)

    return this.request(endpoint, {
      method: 'POST',
      body: formData,
      headers: {}, // Let browser set Content-Type for FormData
      onUploadProgress: onProgress
    })
  }
}

export const apiClient = new APIClient()
```

### **Analytics Service**
```javascript
// services/analytics.js
export const analyticsAPI = {
  getKPISummary: (daysBack = 30) =>
    apiClient.get('/kpis/summary', { days_back: daysBack }),

  getRevenueTrend: (daysBack = 30, interval = 'daily') =>
    apiClient.get('/kpis/revenue-trend', { days_back: daysBack, interval }),

  getTopProducts: (daysBack = 30, limit = 5) =>
    apiClient.get('/kpis/top-products', { days_back: daysBack, limit })
}
```

### **Upload Service**
```javascript
// services/upload.js
export const uploadAPI = {
  uploadCSV: (file, onProgress) =>
    apiClient.upload('/upload/csv', file, onProgress),

  connectGoogleSheets: (url, sheetName = 'Sheet1') =>
    apiClient.post('/admin/connect-sheets', {
      spreadsheet_url: url,
      sheet_name: sheetName
    }),

  validateSheetsURL: (url) =>
    apiClient.get('/admin/validate-sheets', { url })
}
```

---

## 🎣 Custom Hooks

### **useAnalytics Hook**
```javascript
// hooks/useAnalytics.js
export const useAnalytics = (daysBack = 30) => {
  const kpiQuery = useQuery({
    queryKey: ['kpis', daysBack],
    queryFn: () => analyticsAPI.getKPISummary(daysBack),
    staleTime: 5 * 60 * 1000, // 5 minutes
    refetchInterval: 5 * 60 * 1000
  })

  const trendQuery = useQuery({
    queryKey: ['trend', daysBack],
    queryFn: () => analyticsAPI.getRevenueTrend(daysBack),
    staleTime: 5 * 60 * 1000
  })

  return {
    kpis: kpiQuery.data,
    trend: trendQuery.data?.trend_data || [],
    isLoading: kpiQuery.isLoading || trendQuery.isLoading,
    error: kpiQuery.error || trendQuery.error,
    refetch: () => {
      kpiQuery.refetch()
      trendQuery.refetch()
    }
  }
}
```

### **useUpload Hook**
```javascript
// hooks/useUpload.js
export const useUpload = () => {
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState('idle') // idle, uploading, success, error
  const [result, setResult] = useState(null)

  const uploadCSV = useMutation({
    mutationFn: (file) => uploadAPI.uploadCSV(file, setProgress),
    onMutate: () => {
      setStatus('uploading')
      setProgress(0)
    },
    onSuccess: (data) => {
      setStatus('success')
      setResult(data)
      setProgress(100)
    },
    onError: (error) => {
      setStatus('error')
      setResult({ error: error.message })
    }
  })

  const connectSheets = useMutation({
    mutationFn: ({ url, sheetName }) => 
      uploadAPI.connectGoogleSheets(url, sheetName),
    onSuccess: (data) => {
      setStatus('success')
      setResult(data)
    },
    onError: (error) => {
      setStatus('error')
      setResult({ error: error.message })
    }
  })

  return {
    uploadCSV: uploadCSV.mutate,
    connectSheets: connectSheets.mutate,
    progress,
    status,
    result,
    reset: () => {
      setStatus('idle')
      setProgress(0)
      setResult(null)
    }
  }
}
```

---

## 🎨 Styling System

### **Tailwind Configuration**
```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8'
        },
        success: {
          50: '#ecfdf5',
          500: '#10b981',
          600: '#059669'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif']
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out'
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography')
  ]
}
```

### **Component Style Patterns**
```javascript
// utils/styles.js
export const cardStyles = {
  base: 'bg-white overflow-hidden shadow rounded-lg',
  padding: 'p-5',
  hover: 'hover:shadow-md transition-shadow duration-200'
}

export const buttonStyles = {
  primary: 'bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md',
  secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-900 font-medium py-2 px-4 rounded-md',
  danger: 'bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-md'
}
```

---

## 🔄 State Management

### **React Query Configuration**
```javascript
// providers/QueryProvider.jsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
      retry: (failureCount, error) => {
        if (error.status === 404) return false
        return failureCount < 3
      }
    },
    mutations: {
      retry: 1
    }
  }
})

export const QueryProvider = ({ children }) => (
  <QueryClientProvider client={queryClient}>
    {children}
    <ReactQueryDevtools initialIsOpen={false} />
  </QueryClientProvider>
)
```

### **Global State Context**
```javascript
// contexts/AppContext.jsx
const AppContext = createContext()

export const AppProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [preferences, setPreferences] = useState({
    theme: 'light',
    defaultTimeframe: 30,
    currency: 'USD'
  })

  const value = {
    user,
    setUser,
    preferences,
    updatePreferences: (updates) => 
      setPreferences(prev => ({ ...prev, ...updates }))
  }

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useApp must be used within AppProvider')
  }
  return context
}
```

---

## 🧪 Testing Strategy

### **Component Testing Template**
```javascript
// __tests__/components/KPICard.test.jsx
import { render, screen } from '@testing-library/react'
import { KPICard } from '../KPICard'

describe('KPICard', () => {
  const defaultProps = {
    title: 'Total Revenue',
    value: 12345.67,
    format: 'currency'
  }

  it('displays formatted value correctly', () => {
    render(<KPICard {...defaultProps} />)
    
    expect(screen.getByText('Total Revenue')).toBeInTheDocument()
    expect(screen.getByText('$12,345.67')).toBeInTheDocument()
  })

  it('shows trend indicator when change provided', () => {
    render(<KPICard {...defaultProps} change={15.5} />)
    
    expect(screen.getByText('15.5%')).toBeInTheDocument()
    expect(screen.getByTestId('trend-up')).toBeInTheDocument()
  })

  it('handles loading state', () => {
    render(<KPICard {...defaultProps} loading />)
    
    expect(screen.getByTestId('loading-skeleton')).toBeInTheDocument()
  })
})
```

### **API Integration Testing**
```javascript
// __tests__/hooks/useAnalytics.test.js
import { renderHook, waitFor } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useAnalytics } from '../useAnalytics'
import { analyticsAPI } from '../../services/analytics'

jest.mock('../../services/analytics')

const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  })
  return ({ children }) => (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  )
}

describe('useAnalytics', () => {
  it('fetches KPI data successfully', async () => {
    const mockData = {
      total_revenue: 12345.67,
      total_sales_count: 150,
      average_order_value: 82.30
    }
    
    analyticsAPI.getKPISummary.mockResolvedValue(mockData)
    
    const { result } = renderHook(() => useAnalytics(30), {
      wrapper: createWrapper()
    })

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false)
    })

    expect(result.current.kpis).toEqual(mockData)
    expect(analyticsAPI.getKPISummary).toHaveBeenCalledWith(30)
  })
})
```

---

## 🚀 Performance Optimization

### **Code Splitting**
```javascript
// App.jsx
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Upload = lazy(() => import('./pages/Upload'))
const Admin = lazy(() => import('./pages/Admin'))

function App() {
  return (
    <Router>
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/admin" element={<Admin />} />
        </Routes>
      </Suspense>
    </Router>
  )
}
```

### **Memoization Strategy**
```javascript
// components/Dashboard.jsx
const Dashboard = () => {
  const { kpis, trend, isLoading } = useAnalytics(30)
  
  // Memoize expensive calculations
  const chartData = useMemo(() => {
    if (!trend) return null
    return processChartData(trend)
  }, [trend])
  
  // Memoize components that don't change often
  const kpiCards = useMemo(() => 
    kpis ? renderKPICards(kpis) : null,
    [kpis]
  )

  if (isLoading) return <DashboardSkeleton />

  return (
    <div className="space-y-6">
      {kpiCards}
      <RevenueChart data={chartData} />
    </div>
  )
}
```

---

This technical specification provides the detailed implementation guidance you need to build a professional, performant React dashboard. Each component is designed to be reusable, testable, and maintainable.

**Ready to start coding?** Pick any component or feature from this spec and we can implement it step by step!