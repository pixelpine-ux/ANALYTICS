import { useState, useEffect } from 'react'

export const TestDashboard = () => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('Fetching from:', 'http://localhost:8000/api/v1/dashboard/kpis?days=30')
        
        const response = await fetch('http://localhost:8000/api/v1/dashboard/kpis?days=30', {
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          mode: 'cors'
        })
        
        console.log('Response status:', response.status)
        console.log('Response headers:', response.headers)
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }
        
        const result = await response.json()
        console.log('API Response:', result)
        setData(result)
        
      } catch (err) {
        console.error('Fetch error:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold mb-4">Loading...</h1>
        <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold text-red-600 mb-4">Error</h1>
        <p className="text-red-500 mb-4">{error}</p>
        <button 
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Retry
        </button>
      </div>
    )
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">API Test Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-lg shadow border">
          <h3 className="text-sm text-gray-600">Revenue</h3>
          <p className="text-2xl font-bold">${data?.revenue || 0}</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border">
          <h3 className="text-sm text-gray-600">Profit Margin</h3>
          <p className="text-2xl font-bold">{data?.profit_margin || 0}%</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border">
          <h3 className="text-sm text-gray-600">Avg Order Value</h3>
          <p className="text-2xl font-bold">${data?.avg_order_value || 0}</p>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow border">
          <h3 className="text-sm text-gray-600">Repeat Customers</h3>
          <p className="text-2xl font-bold">{data?.repeat_customers || 0}</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow border">
        <h2 className="text-lg font-semibold mb-4">Raw API Response</h2>
        <pre className="bg-gray-100 p-4 rounded text-sm overflow-auto">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    </div>
  )
}