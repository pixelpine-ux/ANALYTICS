import { useState } from 'react';
import { DollarSign, TrendingUp, Users, ShoppingCart } from 'lucide-react';
import KPICard from './components/KPICard';
import RevenueChart from './components/RevenueChart';
import SaleForm from './components/SaleForm';
import CSVImport from './components/CSVImport';

function App() {
  const [isLoading, setIsLoading] = useState(false);

  const kpiData = [
    { title: 'Total Revenue', value: '$24,847', trend: 12.8, icon: DollarSign },
    { title: 'Profit Margin', value: '18.2%', trend: -2.4, icon: TrendingUp },
    { title: 'Active Customers', value: '1,247', trend: 8.6, icon: Users },
    { title: 'Total Orders', value: '892', trend: 15.3, icon: ShoppingCart }
  ];

  const chartData = [
    { date: '2024-11-23', revenue: 2400 },
    { date: '2024-11-24', revenue: 1398 },
    { date: '2024-11-25', revenue: 9800 },
    { date: '2024-11-26', revenue: 3908 },
    { date: '2024-11-27', revenue: 4800 },
    { date: '2024-11-28', revenue: 3800 },
    { date: '2024-11-29', revenue: 4300 },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="space-y-8">
          
          {/* Header */}
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900">Business Analytics</h1>
            <p className="text-gray-600 mt-2">Real-time insights for data-driven decisions</p>
          </div>

          {/* KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {kpiData.map((kpi, index) => (
              <KPICard key={index} {...kpi} />
            ))}
          </div>

          {/* Main Content */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <RevenueChart data={chartData} isLoading={isLoading} />
            </div>
            <div>
              <SaleForm onSaleAdded={() => {}} isSubmitting={isLoading} />
            </div>
          </div>

          {/* Bottom Section */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <CSVImport onImportComplete={() => {}} />
            
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="font-semibold mb-4">Today's Summary</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center p-3 bg-green-50 rounded">
                  <div className="text-2xl font-bold text-green-700">12</div>
                  <div className="text-sm text-green-600">Sales</div>
                </div>
                <div className="text-center p-3 bg-blue-50 rounded">
                  <div className="text-2xl font-bold text-blue-700">8</div>
                  <div className="text-sm text-blue-600">Customers</div>
                </div>
              </div>
            </div>
            
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="font-semibold mb-4">Recent Activity</h3>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">iPhone 15 Pro</span>
                  <span className="font-semibold">$1,199</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">AirPods Pro</span>
                  <span className="font-semibold">$249</span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;