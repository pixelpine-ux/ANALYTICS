import { useState, useEffect } from 'react'

export const SimpleDashboard = () => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/dashboard/kpis?days=30')
      .then(response => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        return response.json()
      })
      .then(data => {
        console.log('Success:', data)
        setData(data)
        setLoading(false)
      })
      .catch(error => {
        console.error('Error:', error)
        setError(error.message)
        setLoading(false)
      })
  }, [])

  if (loading) return <div className="p-8">Loading...</div>
  if (error) return <div className="p-8 text-red-600">Error: {error}</div>

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-8">Analytics Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-sm text-gray-600 mb-2">💰 Total Revenue</h3>
          <p className="text-3xl font-bold text-gray-900">
            ${data?.revenue?.toLocaleString() || '0'}
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-sm text-gray-600 mb-2">📊 Profit Margin</h3>
          <p className="text-3xl font-bold text-gray-900">
            {data?.profit_margin?.toFixed(1) || '0'}%
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-sm text-gray-600 mb-2">🛒 Avg Order Value</h3>
          <p className="text-3xl font-bold text-gray-900">
            ${data?.avg_order_value?.toLocaleString() || '0'}
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-sm text-gray-600 mb-2">👥 Repeat Customers</h3>
          <p className="text-3xl font-bold text-gray-900">
            {data?.repeat_customers || '0'}
          </p>
        </div>
      </div>

      {data?.top_products && (
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b">
            <h2 className="text-xl font-semibold">🏆 Top Products</h2>
          </div>
          <div className="p-6">
            {data.top_products.map((product, index) => (
              <div key={product.product_name} className="flex justify-between items-center py-2 border-b last:border-b-0">
                <span className="font-medium">{index + 1}. {product.product_name}</span>
                <div className="text-right">
                  <div className="font-bold">${product.total_revenue}</div>
                  <div className="text-sm text-gray-500">{product.total_sales} sales</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="mt-8 bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-4">Raw API Data</h3>
        <pre className="bg-gray-100 p-4 rounded text-sm overflow-auto">
          {JSON.stringify(data, null, 2)}
        </pre>
      </div>
    </div>
  )
}