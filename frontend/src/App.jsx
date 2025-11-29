import { useState, useEffect } from 'react';
import { DollarSign, TrendingUp, Users, ShoppingCart } from 'lucide-react';
import KPICard from './components/KPICard';
import RevenueChart from './components/RevenueChart';
import SaleForm from './components/SaleForm';
import CSVImport from './components/CSVImport';
import DashboardLayout from './layouts/DashboardLayout';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(new Date());

  const handleRefresh = () => {
    setIsLoading(true);
    setTimeout(() => {
      setLastUpdated(new Date());
      setIsLoading(false);
    }, 1500);
  };

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
    <DashboardLayout
      lastUpdated={lastUpdated}
      onRefresh={handleRefresh}
      isLoading={isLoading}
    >
      <div className="section-spacing container-main">
        
        <div className="text-center component-spacing">
          <h1 className="text-3xl font-bold text-gray-900">
            Business Analytics
          </h1>
          <p className="text-gray-500">
            Real-time insights for data-driven decisions
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 grid-spacing component-spacing">
          {kpiData.map((kpi, index) => (
            <KPICard key={index} {...kpi} />
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 grid-spacing component-spacing">
          <div className="lg:col-span-2">
            <RevenueChart data={chartData} isLoading={isLoading} />
          </div>
          <div>
            <SaleForm onSaleAdded={() => {}} isSubmitting={isLoading} />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 grid-spacing">
          <div>
            <CSVImport onImportComplete={() => {}} />
          </div>
          <div className="card-default">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Today's Summary</h3>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-3 bg-green-100 rounded-lg">
                <div className="text-2xl font-bold text-green-700">12</div>
                <div className="text-sm text-green-800">Sales</div>
              </div>
              <div className="text-center p-3 bg-blue-100 rounded-lg">
                <div className="text-2xl font-bold text-blue-700">8</div>
                <div className="text-sm text-blue-800">Customers</div>
              </div>
            </div>
          </div>
          <div className="card-default">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Activity</h3>
            <div className="flex flex-col gap-3">
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
    </DashboardLayout>
  );
}

export default App;