import { LineChart, Line, XAxis, YAxis, ResponsiveContainer, Tooltip } from 'recharts';
import { TrendingUp, Table } from 'lucide-react';
import { useState } from 'react';

function RevenueChart({ data, isLoading, title = "Revenue Trend", description = "Last 7 days performance" }) {
  const [showDataTable, setShowDataTable] = useState(false);
  // Loading state with accessibility
  if (isLoading) {
    return (
      <div 
        className="card card-padding h-80"
        role="status"
        aria-live="polite"
        aria-label="Loading revenue chart data"
      >
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-48 mb-4"></div>
          <div className="h-64 bg-gray-100 rounded"></div>
        </div>
        <span className="sr-only">Loading chart data, please wait...</span>
      </div>
    );
  }

  // Empty state with accessibility
  if (!data || data.length === 0) {
    return (
      <div 
        className="card card-padding h-80 flex items-center justify-center"
        role="status"
        aria-live="polite"
      >
        <div className="text-center">
          <TrendingUp className="w-12 h-12 text-gray-300 mx-auto mb-4" aria-hidden="true" />
          <h3 className="text-lg font-semibold text-gray-600 mb-2">
            No Data Available
          </h3>
          <p className="text-gray-400">
            Start adding sales to see your revenue trends
          </p>
        </div>
      </div>
    );
  }

  // Custom tooltip (clean, minimal)
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 rounded-lg shadow-lg border border-gray-200">
          <p className="text-sm text-gray-700 mb-1 font-medium">
            {new Date(label).toLocaleDateString()}
          </p>
          <p className="text-xl font-bold text-gray-900">
            ${payload[0].value.toFixed(2)}
          </p>
        </div>
      );
    }
    return null;
  };

  // Calculate summary statistics for screen readers
  const totalRevenue = data.reduce((sum, item) => sum + item.revenue, 0);
  const avgRevenue = totalRevenue / data.length;
  const maxRevenue = Math.max(...data.map(item => item.revenue));
  const minRevenue = Math.min(...data.map(item => item.revenue));
  
  const chartId = `chart-${title.toLowerCase().replace(/\s+/g, '-')}`;
  const tableId = `table-${title.toLowerCase().replace(/\s+/g, '-')}`;

  return (
    <div className="card-default relative z-10">
      {/* Header */}
      <div className="flex items-start justify-between component-spacing-sm">
        <div className="flex-1 min-w-0 pr-4">
          <h3 
            className="text-xl font-bold text-gray-900 leading-tight mb-1"
            id={`${chartId}-title`}
          >
            {title}
          </h3>
          <p 
            className="text-base text-gray-700 leading-relaxed"
            id={`${chartId}-description`}
          >
            {description}
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowDataTable(!showDataTable)}
            className="p-2 text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-amber-400 rounded"
            aria-label={showDataTable ? 'Hide data table' : 'Show data table'}
            aria-expanded={showDataTable}
            aria-controls={tableId}
          >
            <Table className="w-4 h-4" />
          </button>
          <TrendingUp className="w-5 h-5 text-amber-400" aria-hidden="true" />
        </div>
      </div>

      {/* Screen reader summary */}
      <div className="sr-only" aria-live="polite">
        Chart showing {title.toLowerCase()} with {data.length} data points. 
        Total revenue: ${totalRevenue.toFixed(2)}. 
        Average: ${avgRevenue.toFixed(2)}. 
        Highest: ${maxRevenue.toFixed(2)}. 
        Lowest: ${minRevenue.toFixed(2)}.
      </div>

      {/* Chart */}
      <div 
        className="h-48"
        role="img"
        aria-labelledby={`${chartId}-title`}
        aria-describedby={`${chartId}-description ${chartId}-summary`}
      >
        <div id={`${chartId}-summary`} className="sr-only">
          Line chart displaying revenue data from {new Date(data[0]?.date).toLocaleDateString()} 
          to {new Date(data[data.length - 1]?.date).toLocaleDateString()}. 
          Use the data table button to access detailed information.
        </div>
        
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
            <XAxis 
              dataKey="date" 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 13, fill: '#374151', fontWeight: 500 }}
              tickFormatter={(date) => new Date(date).toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric' 
              })}
            />
            <YAxis 
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 13, fill: '#374151', fontWeight: 500 }}
              tickFormatter={(value) => `$${value}`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Line 
              type="monotone" 
              dataKey="revenue" 
              stroke="#fbbf24" 
              strokeWidth={2}
              dot={{ fill: '#fbbf24', strokeWidth: 0, r: 4 }}
              activeDot={{ r: 6, stroke: '#fbbf24', strokeWidth: 2, fill: '#fff' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Accessible Data Table */}
      {showDataTable && (
        <div className="component-spacing border-t pt-6">
          <h4 className="text-sm font-semibold text-gray-700 mb-3">
            Revenue Data Table
          </h4>
          <div className="overflow-x-auto">
            <table 
              id={tableId}
              className="min-w-full text-sm"
              role="table"
              aria-label="Revenue data in tabular format"
            >
              <thead>
                <tr className="border-b border-gray-200">
                  <th 
                    className="text-left py-2 px-3 font-medium text-gray-700"
                    scope="col"
                  >
                    Date
                  </th>
                  <th 
                    className="text-right py-2 px-3 font-medium text-gray-700"
                    scope="col"
                  >
                    Revenue
                  </th>
                </tr>
              </thead>
              <tbody>
                {data.map((item, index) => (
                  <tr key={index} className="border-b border-gray-100">
                    <td className="py-2 px-3 text-gray-600">
                      {new Date(item.date).toLocaleDateString()}
                    </td>
                    <td className="py-2 px-3 text-right font-medium text-gray-800">
                      ${item.revenue.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
              <tfoot>
                <tr className="border-t-2 border-gray-300 font-semibold">
                  <td className="py-2 px-3 text-gray-700">
                    Total
                  </td>
                  <td className="py-2 px-3 text-right text-gray-800">
                    ${totalRevenue.toFixed(2)}
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default RevenueChart;