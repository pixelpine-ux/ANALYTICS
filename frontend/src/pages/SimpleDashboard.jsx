import { useState, useEffect } from 'react'
import { KPICard } from '../components/ui/KPICard'
import { RevenueChart } from '../components/charts/RevenueChart'
import { TopProductsChart } from '../components/charts/TopProductsChart'
import { SkeletonCard, SkeletonChart } from '../components/ui/LoadingSpinner'
import { ErrorBoundary, ErrorMessage } from '../components/ui/ErrorBoundary'
import { useToast } from '../components/ui/Toast'

export const SimpleDashboard = () => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [refreshing, setRefreshing] = useState(false)
  const { showToast, ToastContainer } = useToast()

  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/dashboard/kpis?days=30')
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const result = await response.json()
      setData(result)
      setError(null)
      if (refreshing) {
        showToast('Dashboard refreshed successfully')
        setRefreshing(false)
      }
    } catch (err) {
      setError(err.message)
      if (refreshing) {
        showToast('Failed to refresh dashboard', 'error')
        setRefreshing(false)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleRefresh = () => {
    setRefreshing(true)
    fetchData()
  }

  useEffect(() => {
    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="p-8 bg-gradient-to-br from-slate-50 to-slate-100 min-h-screen">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <div className="h-8 bg-slate-200 rounded w-1/3 mb-2 animate-pulse"></div>
            <div className="h-4 bg-slate-200 rounded w-1/2 animate-pulse"></div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {[...Array(4)].map((_, i) => <SkeletonCard key={i} />)}
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <SkeletonChart />
            <SkeletonChart />
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-8 bg-gradient-to-br from-slate-50 to-slate-100 min-h-screen">
        <div className="max-w-2xl mx-auto pt-16">
          <ErrorMessage message={error} onRetry={handleRefresh} />
        </div>
      </div>
    )
  }

  return (
    <ErrorBoundary>
      <div className="p-8 bg-gradient-to-br from-slate-50 to-slate-100 min-h-screen">
        <ToastContainer />
        
        {/* Header */}
        <div className="max-w-7xl mx-auto mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent mb-2">
                Analytics Dashboard
              </h1>
              <p className="text-slate-600 flex items-center">
                <span className="w-2 h-2 bg-emerald-500 rounded-full mr-2 animate-pulse"></span>
                Real-time business insights
              </p>
            </div>
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="px-4 py-2 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 transition-all duration-200 flex items-center space-x-2 shadow-sm hover:shadow-md disabled:opacity-50"
            >
              <span className={`text-lg ${refreshing ? 'animate-spin' : ''}`}>🔄</span>
              <span className="font-medium text-slate-700">{refreshing ? 'Refreshing...' : 'Refresh'}</span>
            </button>
          </div>
        </div>

        <div className="max-w-7xl mx-auto">
          {/* KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <KPICard
              title="Total Revenue"
              value={data?.revenue}
              format="currency"
              change={12.5}
              trend="up"
            />
            <KPICard
              title="Profit Margin"
              value={data?.profit_margin}
              format="percentage"
              change={-2.1}
              trend="down"
            />
            <KPICard
              title="Average Order"
              value={data?.avg_order_value}
              format="currency"
              change={5.8}
              trend="up"
            />
            <KPICard
              title="Repeat Customers"
              value={data?.repeat_customers}
              format="number"
              change={8.3}
              trend="up"
            />
          </div>

          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <ErrorBoundary>
              <RevenueChart days={30} />
            </ErrorBoundary>
            <ErrorBoundary>
              <TopProductsChart data={data?.top_products} />
            </ErrorBoundary>
          </div>

          {/* Top Products Table */}
          {data?.top_products && (
            <div className="bg-white rounded-xl shadow-card border border-slate-200 hover:shadow-soft transition-all duration-200">
              <div className="px-6 py-4 border-b border-slate-200">
                <h2 className="text-xl font-semibold text-slate-900 flex items-center">
                  <span className="w-8 h-8 bg-gradient-to-br from-amber-500 to-amber-600 rounded-lg flex items-center justify-center text-white text-sm mr-3">
                    🏆
                  </span>
                  Top Products
                </h2>
              </div>
              <div className="p-6">
                <div className="space-y-3">
                  {data.top_products.map((product, index) => (
                    <div key={product.product_name} className="flex justify-between items-center p-3 rounded-lg hover:bg-slate-50 transition-colors group">
                      <div className="flex items-center">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold mr-3 ${
                          index === 0 ? 'bg-amber-100 text-amber-800' :
                          index === 1 ? 'bg-slate-100 text-slate-800' :
                          index === 2 ? 'bg-orange-100 text-orange-800' :
                          'bg-slate-50 text-slate-600'
                        }`}>
                          {index + 1}
                        </div>
                        <span className="font-medium text-slate-900 group-hover:text-primary-600 transition-colors">
                          {product.product_name}
                        </span>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-slate-900">${product.total_revenue}</div>
                        <div className="text-sm text-slate-500">{product.total_sales} sales</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </ErrorBoundary>
  )
}