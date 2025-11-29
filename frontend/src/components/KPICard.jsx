function KPICard({ 
  title, 
  value, 
  trend, 
  icon: Icon,
  isLoading = false,
  onClick = null,
  'aria-describedby': ariaDescribedBy
}) {
  // Loading state with accessibility
  if (isLoading) {
    return (
      <div 
        className="card p-6 animate-pulse"
        role="status"
        aria-label={`Loading ${title} data`}
        aria-live="polite"
      >
        <div className="h-4 bg-gray-200 rounded w-24 mb-4"></div>
        <div className="h-12 bg-gray-200 rounded w-32 mb-3"></div>
        <div className="h-4 bg-gray-200 rounded w-20"></div>
        <span className="sr-only">Loading {title} information...</span>
      </div>
    );
  }

  // Trend styling (subtle, not aggressive)
  const getTrendStyle = () => {
    if (!trend) return 'text-gray-400';
    return trend > 0 
      ? 'text-emerald-600 bg-emerald-50' 
      : 'text-red-500 bg-red-50';
  };

  const getTrendIcon = () => {
    if (!trend) return { icon: '', label: '' };
    return trend > 0 
      ? { icon: '↗', label: 'trending up' }
      : { icon: '↘', label: 'trending down' };
  };
  
  const trendInfo = getTrendIcon();
  const cardId = `kpi-${title.toLowerCase().replace(/\s+/g, '-')}`;

  return (
    <div className="card-default group">
        {/* Top section: Title and Icon */}
        <div className="flex items-start justify-between mb-6">
          <h3 
            className="text-sm font-bold text-gray-800 uppercase tracking-wider leading-tight"
            id={`${cardId}-title`}
          >
            {title}
          </h3>
          {Icon && (
            <div className="p-1.5 bg-amber-50 rounded-lg flex-shrink-0">
              <Icon 
                className="w-4 h-4 text-amber-600" 
                aria-hidden="true"
                role="img"
              />
            </div>
          )}
        </div>

        {/* Center: Large value with proper spacing */}
        <div className="mb-6">
          <p 
            className="text-4xl md:text-3xl lg:text-4xl font-black text-gray-900 leading-tight tracking-tight break-all"
            aria-label={`Current value: ${value}`}
          >
            {value}
          </p>
        </div>

        {/* Bottom: Enhanced trend indicator */}
        {trend !== undefined && (
          <div className="flex items-center justify-between">
            <div 
              className={`inline-flex items-center px-3 py-1.5 rounded-full text-xs font-bold ${getTrendStyle()}`}
              role="status"
              aria-label={`Trend: ${trendInfo.label} ${Math.abs(trend).toFixed(1)} percent compared to last week`}
            >
              <span className="mr-1.5" aria-hidden="true">{trendInfo.icon}</span>
              <span>{Math.abs(trend).toFixed(1)}%</span>
              {/* Screen reader only trend description */}
              <span className="sr-only">
                {trend > 0 ? 'increased' : 'decreased'} by {Math.abs(trend).toFixed(1)} percent
              </span>
            </div>
            <span className="text-sm text-gray-600 font-medium">vs last week</span>
          </div>
        )}
        
        {/* Hover glow effect */}
        <div className="absolute inset-0 rounded-[10px] bg-gradient-to-br from-amber-400/10 to-orange-400/10 opacity-0 group-hover:opacity-100 group-focus-within:opacity-100 transition-opacity duration-500 pointer-events-none"></div>
    </div>
  );
}

export default KPICard;