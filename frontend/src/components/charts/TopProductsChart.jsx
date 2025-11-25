import { useState, useEffect } from 'react'
import { Bar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { dashboardAPI } from '../../services/api'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

export const TopProductsChart = ({ limit = 5 }) => {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await dashboardAPI.getProductPerformance(limit)
        setProducts(result.slice(0, limit))
      } catch (error) {
        console.error('Failed to fetch product performance:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [limit])

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow border border-gray-100">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="space-y-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="flex justify-between">
                <div className="h-4 bg-gray-200 rounded w-1/3"></div>
                <div className="h-4 bg-gray-200 rounded w-1/4"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if (!products.length) {
    return (
      <div className="bg-white p-6 rounded-lg shadow border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Products</h3>
        <p className="text-gray-500 text-center py-8">No product data available</p>
      </div>
    )
  }

  const chartData = {
    labels: products.map(p => p.product_name),
    datasets: [
      {
        label: 'Revenue',
        data: products.map(p => p.total_revenue),
        backgroundColor: [
          '#2563eb',
          '#3b82f6',
          '#60a5fa',
          '#93c5fd',
          '#dbeafe'
        ].slice(0, products.length),
        borderWidth: 0,
        borderRadius: 4
      }
    ]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: 'white',
        bodyColor: 'white',
        callbacks: {
          label: (context) => `Revenue: $${context.parsed.x.toLocaleString()}`
        }
      }
    },
    scales: {
      x: {
        beginAtZero: true,
        grid: {
          color: '#f1f5f9'
        },
        ticks: {
          color: '#64748b',
          callback: (value) => `$${value.toLocaleString()}`
        }
      },
      y: {
        grid: {
          display: false
        },
        ticks: {
          color: '#64748b'
        }
      }
    }
  }

  return (
    <div className="bg-white p-6 rounded-xl shadow-card border border-slate-200 hover:shadow-soft transition-all duration-200">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-slate-900 flex items-center">
            <span className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-lg flex items-center justify-center text-white text-sm mr-3">
              🏆
            </span>
            Top Products
          </h3>
          <p className="text-sm text-slate-500 mt-1">Best performing products by revenue</p>
        </div>
      </div>
      <div className="h-64">
        <Bar data={chartData} options={options} />
      </div>
    </div>
  )
}