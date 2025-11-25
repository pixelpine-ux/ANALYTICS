const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1'

class APIClient {
  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`
    
    try {
      const response = await fetch(url, {
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          ...options.headers 
        },
        mode: 'cors',
        ...options
      })
      
      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(`API Error ${response.status}: ${errorText}`)
      }
      
      return response.json()
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Cannot connect to server. Please ensure the backend is running on http://localhost:8000')
      }
      throw error
    }
  }

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

  upload(endpoint, file) {
    const formData = new FormData()
    formData.append('file', file)
    return this.request(endpoint, {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for FormData
      body: formData
    })
  }
}

export const api = new APIClient()

// Dashboard API endpoints
export const dashboardAPI = {
  getKPIs: (days = 30) => api.get('/dashboard/kpis', { days }),
  getRevenueTrend: (days = 30) => api.get('/dashboard/revenue-trend', { days }),
  getProductPerformance: (limit = 10) => api.get('/dashboard/product-performance', { limit }),
  getCustomerAnalytics: () => api.get('/dashboard/customer-analytics')
}

// Upload API endpoints
export const uploadAPI = {
  uploadSalesCSV: (file) => api.upload('/data/upload-sales-csv', file),
  uploadCustomersCSV: (file) => api.upload('/data/upload-customers-csv', file),
  uploadExpensesCSV: (file) => api.upload('/data/upload-expenses-csv', file)
}

// Data entry API endpoints
export const entryAPI = {
  createSale: (data) => api.post('/entry/quick-sale', data),
  createCustomer: (data) => api.post('/entry/quick-customer', data),
  createExpense: (data) => api.post('/entry/quick-expense', data)
}