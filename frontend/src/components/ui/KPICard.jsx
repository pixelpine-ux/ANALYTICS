const getIcon = (title) => {
  const icons = {
    'Total Revenue': '💰',
    'Total Sales': '📊',
    'Average Order': '🛒',
    'Repeat Customers': '👥'
  }
  return icons[title] || '📈'
}

export const KPICard = ({ title, value, format = 'number', loading = false, change = null }) => {
  if (loading) {
    return (
      <div className="bg-white p-6 rounded-xl shadow-card border border-slate-200 hover:shadow-soft transition-all duration-200">
        <div className="animate-pulse">
          <div className="flex items-center mb-4">
            <div className="w-10 h-10 bg-slate-200 rounded-lg mr-3"></div>
            <div className="h-4 bg-slate-200 rounded w-1/2"></div>
          </div>
          <div className="h-8 bg-slate-200 rounded w-3/4 mb-2"></div>
          <div className="h-3 bg-slate-200 rounded w-1/3"></div>
        </div>
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
    if (change > 0) return 'text-emerald-600 bg-emerald-50'
    if (change < 0) return 'text-red-600 bg-red-50'
    return 'text-slate-500 bg-slate-50'
  }

  const getTrendIcon = (change) => {
    if (change > 0) return '↗️'
    if (change < 0) return '↘️'
    return '➡️'
  }

  return (
    <div className="bg-white p-6 rounded-xl shadow-card border border-slate-200 hover:shadow-soft transition-all duration-200 group">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center text-white text-lg mr-3 group-hover:scale-105 transition-transform">
            {getIcon(title)}
          </div>
          <div>
            <p className="text-sm font-medium text-slate-600 mb-1">{title}</p>
          </div>
        </div>
        {change !== null && (
          <div className={`px-2 py-1 rounded-full text-xs font-medium ${getTrendColor(change)}`}>
            {getTrendIcon(change)} {Math.abs(change).toFixed(1)}%
          </div>
        )}
      </div>
      
      <div className="space-y-1">
        <p className="text-3xl font-bold text-slate-900 tracking-tight">{formatValue(value)}</p>
        <p className="text-xs text-slate-500">Last 30 days</p>
      </div>
    </div>
  )
}