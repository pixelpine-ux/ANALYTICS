import { BarChart3, TrendingUp, DollarSign, Users } from 'lucide-react';
import { useEffect, useRef } from 'react';

function Navigation({ activeTab, onTabChange }) {
  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3, description: 'View key performance indicators and overview' },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp, description: 'Detailed analytics and trends' },
    { id: 'sales', label: 'Sales', icon: DollarSign, description: 'Sales data and transactions' },
    { id: 'customers', label: 'Customers', icon: Users, description: 'Customer information and insights' }
  ];
  
  const navRef = useRef(null);
  
  // Handle keyboard navigation
  const handleKeyDown = (e, tabId) => {
    const currentIndex = tabs.findIndex(tab => tab.id === tabId);
    let nextIndex;
    
    switch (e.key) {
      case 'ArrowRight':
        e.preventDefault();
        nextIndex = (currentIndex + 1) % tabs.length;
        break;
      case 'ArrowLeft':
        e.preventDefault();
        nextIndex = currentIndex === 0 ? tabs.length - 1 : currentIndex - 1;
        break;
      case 'Home':
        e.preventDefault();
        nextIndex = 0;
        break;
      case 'End':
        e.preventDefault();
        nextIndex = tabs.length - 1;
        break;
      default:
        return;
    }
    
    const nextTab = tabs[nextIndex];
    onTabChange(nextTab.id);
    
    // Focus the next tab
    setTimeout(() => {
      const nextButton = navRef.current?.querySelector(`[data-tab="${nextTab.id}"]`);
      nextButton?.focus();
    }, 0);
  };

  return (
    <nav 
      className="bg-white/80 backdrop-blur-sm border-b border-neutral-200 sticky top-0 z-40"
      role="navigation"
      aria-label="Main navigation"
      ref={navRef}
    >
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between py-4">
          {/* Logo/Brand */}
          <div className="flex items-center">
            <BarChart3 
              className="w-8 h-8 text-amber-400 mr-3" 
              aria-hidden="true"
            />
            <h1 className="text-xl font-bold text-gray-800">
              <span className="sr-only">Retail</span> Analytics
            </h1>
          </div>
          
          {/* Navigation Tabs */}
          <div 
            className="flex items-center space-x-1"
            role="tablist"
            aria-label="Dashboard sections"
          >
            {tabs.map((tab, index) => (
              <button
                key={tab.id}
                data-tab={tab.id}
                onClick={() => onTabChange(tab.id)}
                onKeyDown={(e) => handleKeyDown(e, tab.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-amber-400 focus:ring-offset-2 ${
                  activeTab === tab.id
                    ? 'bg-amber-50 text-amber-700 border border-amber-200'
                    : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
                }`}
                role="tab"
                aria-selected={activeTab === tab.id}
                aria-controls={`tabpanel-${tab.id}`}
                aria-describedby={`tab-desc-${tab.id}`}
                tabIndex={activeTab === tab.id ? 0 : -1}
              >
                <tab.icon 
                  className="w-4 h-4" 
                  aria-hidden="true"
                />
                <span className="hidden sm:block">{tab.label}</span>
                {/* Screen reader description */}
                <span 
                  id={`tab-desc-${tab.id}`} 
                  className="sr-only"
                >
                  {tab.description}
                </span>
              </button>
            ))}
          </div>
          
          {/* Status Indicator */}
          <div 
            className="flex items-center text-sm text-gray-500"
            role="status"
            aria-live="polite"
            aria-label="System status: Live and connected"
          >
            <div 
              className="w-2 h-2 bg-emerald-500 rounded-full mr-2 animate-pulse"
              aria-hidden="true"
            ></div>
            <span className="hidden md:block">Live</span>
            <span className="sr-only">System is live and connected</span>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navigation;