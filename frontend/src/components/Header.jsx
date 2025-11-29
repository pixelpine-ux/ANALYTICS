import { RefreshCw } from 'lucide-react';

function Header({ onRefresh, isLoading, lastUpdated }) {
  return (
    <div className="bg-gradient-to-r from-gray-900 to-gray-800 text-white">
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl md:text-4xl font-bold mb-2">
              Business Analytics
            </h1>
            <p className="text-gray-300 text-base md:text-lg">
              Real-time insights for data-driven decisions
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            {lastUpdated && (
              <div className="text-right text-gray-300">
                <p className="text-sm">
                  Last updated: {lastUpdated.toLocaleTimeString()}
                </p>
                <div className="flex items-center justify-end mt-1">
                  <div className="w-2 h-2 bg-emerald-400 rounded-full mr-2 animate-pulse"></div>
                  <span className="text-xs">Live data</span>
                </div>
              </div>
            )}
            
            <button 
              onClick={onRefresh}
              disabled={isLoading}
              className="bg-amber-400 text-white px-4 py-2 rounded-lg hover:bg-amber-500 disabled:opacity-50 transition-all duration-200 font-medium flex items-center"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
              {isLoading ? 'Syncing...' : 'Refresh'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Header;