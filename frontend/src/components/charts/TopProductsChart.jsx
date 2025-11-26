import { useState } from 'react'
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

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export const TopProductsChart = ({ data = [] }) => {
  const [isHovered, setIsHovered] = useState(false)

  if (!data || data.length === 0) {
    return (
      <div className="bg-white p-6 rounded-xl shadow-card border border-slate-200">
        <div className="flex items-center justify-center h-64 text-slate-500">
          <div className="text-center">
            <span className="text-4xl mb-2 block">📊</span>
            <p>No product data available</p>
          </div>
        </div>
      </div>
    )
  }

  const chartData = {
    labels: data.slice(0, 5).map(item => item.product_name),
    datasets: [
      {
        label: 'Revenue',
        data: data.slice(0, 5).map(item => item.total_revenue),
        backgroundColor: [
          'rgba(59, 130, 246, 0.8)',
          'rgba(16, 185, 129, 0.8)',
          'rgba(245, 158, 11, 0.8)',
          'rgba(239, 68, 68, 0.8)',
          'rgba(139, 92, 246, 0.8)'
        ],
        borderColor: [
          'rgb(59, 130, 246)',
          'rgb(16, 185, 129)',
          'rgb(245, 158, 11)',
          'rgb(239, 68, 68)',
          'rgb(139, 92, 246)'
        ],
        borderWidth: 2,
        borderRadius: 8,
        borderSkipped: false,
        hoverBackgroundColor: [
          'rgba(59, 130, 246, 0.9)',
          'rgba(16, 185, 129, 0.9)',
          'rgba(245, 158, 11, 0.9)',
          'rgba(239, 68, 68, 0.9)',
          'rgba(139, 92, 246, 0.9)'
        ]
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
          color: '#64748b',
          maxRotation: 45
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
    },
    animation: {
      duration: 1200,
      easing: 'easeOutQuart',
      delay: (context) => context.dataIndex * 100
    },
    hover: {
      animationDuration: 300
    }
  }

  return (
    <div 
      className={`bg-white p-6 rounded-xl shadow-card border border-slate-200 hover:shadow-soft transition-all duration-300 ${isHovered ? 'border-primary-200' : ''}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="text-lg font-semibold text-slate-900 flex items-center">
            <span className={`w-8 h-8 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-lg flex items-center justify-center text-white text-sm mr-3 transition-transform duration-300 ${isHovered ? 'scale-110' : ''}`}>
              📊
            </span>
            Top Products
          </h3>
          <p className="text-sm text-slate-500 mt-1">Revenue by product</p>
        </div>
      </div>
      <div className="h-64">
        <Bar data={chartData} options={options} />
      </div>
    </div>
  )
}