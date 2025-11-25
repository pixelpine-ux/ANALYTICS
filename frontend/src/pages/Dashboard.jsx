import { useState, useEffect } from 'react'
import { KPICard } from '../components/ui/KPICard'
import { RevenueChart } from '../components/charts/RevenueChart'
import { TopProductsChart } from '../components/charts/TopProductsChart'
import { dashboardAPI } from '../services/api'

export const Dashboard = () => {
  const [kpis, setKpis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [timeframe, setTimeframe] = useState(30)

  useEffect(() => {
    const fetchKPIs = async () => {
      try {
        setLoading(true)
        console.log('Fetching KPIs for timeframe:', timeframe)
        console.log('API URL:', `http://localhost:8000/api/v1/dashboard/kpis?days=${timeframe}`)
        
        const data = await dashboardAPI.getKPIs(timeframe)
        console.log('KPI Response:', data)
        setKpis(data)
        setError(null)
      } catch (err) {
        console.error('KPI Fetch Error:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchKPIs()
  }, [timeframe])

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Unable to load dashboard</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <div className="bg-gray-100 p-4 rounded text-sm text-left mb-4">
            <p><strong>Debug Info:</strong></p>
            <p>API URL: http://localhost:8000/api/v1/dashboard/kpis</p>
            <p>Check browser console for details</p>
          </div>
          <button 
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-slate-200/60 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
                Analytics Dashboard
              </h1>
              <p className="mt-1 text-slate-600 flex items-center">
                <span className="w-2 h-2 bg-emerald-500 rounded-full mr-2 animate-pulse"></span>
                Live insights for the last {timeframe} days
              </p>
            </div>
            
            {/* Time Period Selector */}
            <div className="flex bg-slate-100 rounded-xl p-1">
              {[7, 30, 90].map(days => (
                <button
                  key={days}
                  onClick={() => setTimeframe(days)}
                  className={`px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 ${
                    timeframe === days
                      ? 'bg-white text-primary-600 shadow-sm'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                  }`}
                >
                  {days} days
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          <KPICard
            title="Total Revenue"
            value={kpis?.revenue}
            format="currency"
            loading={loading}
          />
          <KPICard
            title="Total Sales"
            value={kpis?.top_products?.[0]?.total_sales || 0}
            format="number"
            loading={loading}
          />
          <KPICard
            title="Average Order"
            value={kpis?.avg_order_value}
            format="currency"
            loading={loading}
          />
          <KPICard
            title="Repeat Customers"
            value={kpis?.repeat_customers}
            format="number"
            loading={loading}
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <RevenueChart days={timeframe} />
          <TopProductsChart limit={5} />
        </div>

        {/* Top Products Table */}
        {kpis?.top_products && (
          <div className="bg-white rounded-lg shadow border border-gray-100">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Product Performance</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Product
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Revenue
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Sales Count
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {kpis.top_products.slice(0, 10).map((product, index) => (
                    <tr key={product.product_name} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <span className="text-sm font-medium text-gray-900 mr-2">
                            {index + 1}.
                          </span>
                          <span className="text-sm text-gray-900">{product.product_name}</span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        ${product.total_revenue.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {product.sales_count}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}