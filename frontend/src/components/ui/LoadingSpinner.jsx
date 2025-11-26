export const LoadingSpinner = ({ size = 'md', className = '' }) => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
    xl: 'w-12 h-12'
  }

  return (
    <div className={`${sizes[size]} ${className}`}>
      <div className="animate-spin rounded-full border-2 border-gray-300 border-t-primary-600"></div>
    </div>
  )
}

export const SkeletonCard = () => (
  <div className="bg-white p-6 rounded-xl shadow-card border border-slate-200 animate-pulse">
    <div className="flex items-center mb-4">
      <div className="w-10 h-10 bg-slate-200 rounded-lg mr-3"></div>
      <div className="h-4 bg-slate-200 rounded w-1/2"></div>
    </div>
    <div className="h-8 bg-slate-200 rounded w-3/4 mb-2"></div>
    <div className="h-3 bg-slate-200 rounded w-1/3"></div>
  </div>
)

export const SkeletonChart = () => (
  <div className="bg-white p-6 rounded-xl shadow-card border border-slate-200 animate-pulse">
    <div className="h-6 bg-slate-200 rounded w-1/3 mb-6"></div>
    <div className="h-64 bg-slate-100 rounded"></div>
  </div>
)