import { useState, useEffect } from 'react'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { dashboardAPI } from '../../services/api'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

export const RevenueChart = ({ days = 30 }) => {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await dashboardAPI.getRevenueTrend(days)
        setData(result)
      } catch (error) {
        console.error('Failed to fetch revenue trend:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [days])

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow border border-gray-100">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-64 bg-gray-100 rounded"></div>
        </div>
      </div>
    )
  }

  const chartData = {
    labels: data.map(item => new Date(item.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Daily Revenue',
        data: data.map(item => item.revenue),
        borderColor: '#2563eb',
        backgroundColor: 'rgba(37, 99, 235, 0.1)',
        fill: true,
        tension: 0.4,
        pointRadius: 3,
        pointHoverRadius: 6
      }
    ]
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: 'white',
        bodyColor: 'white',
        callbacks: {
          label: (context) => `Revenue: $${context.parsed.y.toLocaleString()}`
        }
      }
    },
    scales: {
      x: {
        grid: {
          display: false
        },
        ticks: {
          color: '#64748b'
        }
      },
      y: {
        beginAtZero: true,
        grid: {
          color: '#f1f5f9'
        },
        ticks: {
          color: '#64748b',
          callback: (value) => `$${value.toLocaleString()}`
        }
      }
    }
  }

  return (
    <div className="bg-white p-6 rounded-xl shadow-card border border-slate-200 hover:shadow-soft transition-all duration-200">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-slate-900 flex items-center">
            <span className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center text-white text-sm mr-3">
              📈
            </span>
            Revenue Trend
          </h3>
          <p className="text-sm text-slate-500 mt-1">Daily revenue over time</p>
        </div>
      </div>
      <div className="h-64">
        <Line data={chartData} options={options} />
      </div>
    </div>
  )
}