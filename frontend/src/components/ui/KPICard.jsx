import { useState } from 'react'

const getIcon = (title) => {
  const icons = {
    'Total Revenue': '💰',
    'Total Sales': '📊',
    'Average Order': '🛒',
    'Repeat Customers': '👥',
    'Profit Margin': '📈'
  }
  return icons[title] || '📊'
}

export const KPICard = ({ title, value, format = 'number', loading = false, change = null, trend = null }) => {
  const [isHovered, setIsHovered] = useState(false)

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-xl shadow-card border border-slate-200 animate-pulse">
        <div className="flex items-center mb-4">
          <div className="w-12 h-12 bg-slate-200 rounded-xl mr-3"></div>
          <div className="h-4 bg-slate-200 rounded w-1/2"></div>
        </div>
        <div className="h-10 bg-slate-200 rounded w-3/4 mb-2"></div>
        <div className="h-3 bg-slate-200 rounded w-1/3"></div>
      </div>
    )
  }

  const formatValue = (val) => {
    if (val === null || val === undefined) return '—'
    
    switch (format) {
      case 'currency':
        return new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 0,
          maximumFractionDigits: 0
        }).format(val)
      case 'percentage':
        return `${val.toFixed(1)}%`
      case 'number':
      default:
        return val.toLocaleString()
    }
  }

  const getTrendColor = (change) => {
    if (change > 0) return 'text-emerald-700 bg-emerald-100 border border-emerald-200'
    if (change < 0) return 'text-red-700 bg-red-100 border border-red-200'
    return 'text-slate-600 bg-slate-100 border border-slate-200'
  }

  const getTrendIcon = (change) => {
    if (change > 0) return '↗️'
    if (change < 0) return '↘️'
    return '➡️'
  }

  return (
    <div 
      className="bg-white p-6 rounded-xl shadow-card border border-slate-200 hover:shadow-soft hover:border-primary-200 transition-all duration-300 group cursor-pointer transform hover:-translate-y-1"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-center">
          <div className={`w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center text-white text-lg mr-4 transition-all duration-300 ${isHovered ? 'scale-110 rotate-3' : ''}`}>
            {getIcon(title)}
          </div>
          <div>
            <p className="text-sm font-medium text-slate-600 mb-1">{title}</p>
            {trend && (
              <div className="flex items-center space-x-1">
                <div className={`w-2 h-2 rounded-full ${trend === 'up' ? 'bg-emerald-500' : trend === 'down' ? 'bg-red-500' : 'bg-slate-400'}`}></div>
                <span className="text-xs text-slate-500">
                  {trend === 'up' ? 'Trending up' : trend === 'down' ? 'Trending down' : 'Stable'}
                </span>
              </div>
            )}
          </div>
        </div>
        {change !== null && (
          <div className={`px-3 py-1 rounded-full text-xs font-medium transition-all duration-200 ${getTrendColor(change)} ${isHovered ? 'scale-105' : ''}`}>
            {getTrendIcon(change)} {Math.abs(change).toFixed(1)}%
          </div>
        )}
      </div>
      
      <div className="space-y-2">
        <p className={`text-3xl font-bold text-slate-900 tracking-tight transition-all duration-300 ${isHovered ? 'text-primary-600' : ''}`}>
          {formatValue(value)}
        </p>
        <p className="text-xs text-slate-500 flex items-center">
          <span className="w-1 h-1 bg-slate-400 rounded-full mr-2"></span>
          Last 30 days
        </p>
      </div>
    </div>
  )
}