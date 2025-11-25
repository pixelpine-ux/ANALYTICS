import { useState } from 'react'
import { FileUpload } from '../components/forms/FileUpload'

export const Upload = () => {
  const [uploadSuccess, setUploadSuccess] = useState(false)

  const handleUploadSuccess = (result) => {
    setUploadSuccess(true)
    // Auto-redirect to dashboard after 3 seconds
    setTimeout(() => {
      window.location.href = '/'
    }, 3000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-slate-200/60">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center">
              <span className="text-white text-lg">📄</span>
            </div>
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
                Upload Data
              </h1>
              <p className="mt-1 text-slate-600">
                Import your sales data to generate analytics insights
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <FileUpload onSuccess={handleUploadSuccess} />

        {uploadSuccess && (
          <div className="mt-8 text-center">
            <div className="inline-flex items-center px-6 py-3 bg-success-100 text-success-800 rounded-lg">
              <span className="text-xl mr-2">🎉</span>
              <span className="font-medium">
                Data uploaded successfully! Redirecting to dashboard...
              </span>
            </div>
          </div>
        )}

        {/* CSV Format Guide */}
        <div className="mt-12 bg-white rounded-lg shadow border border-gray-100">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">CSV Format Requirements</h2>
          </div>
          <div className="p-6">
            <div className="grid md:grid-cols-2 gap-6">
              {/* Required Format */}
              <div>
                <h3 className="font-medium text-gray-900 mb-3">Required Columns</h3>
                <div className="bg-gray-50 p-4 rounded-lg font-mono text-sm">
                  <div className="text-gray-600 mb-2">Header row:</div>
                  <div className="font-semibold">date,product_name,amount</div>
                  
                  <div className="text-gray-600 mt-4 mb-2">Example data:</div>
                  <div className="space-y-1">
                    <div>2024-01-15,Coffee,5.99</div>
                    <div>2024-01-16,Sandwich,8.50</div>
                    <div>2024-01-17,Salad,12.00</div>
                  </div>
                </div>
              </div>

              {/* Optional Format */}
              <div>
                <h3 className="font-medium text-gray-900 mb-3">With Optional Columns</h3>
                <div className="bg-gray-50 p-4 rounded-lg font-mono text-sm">
                  <div className="text-gray-600 mb-2">Full format:</div>
                  <div className="font-semibold text-xs">date,product_name,amount,customer_id,category</div>
                  
                  <div className="text-gray-600 mt-4 mb-2">Example data:</div>
                  <div className="space-y-1 text-xs">
                    <div>2024-01-15,Coffee,5.99,CUST001,beverages</div>
                    <div>2024-01-16,Sandwich,8.50,CUST002,food</div>
                    <div>2024-01-17,Salad,12.00,CUST001,food</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Format Notes */}
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <h4 className="font-medium text-blue-900 mb-2">Format Notes</h4>
              <ul className="text-sm text-blue-800 space-y-1">
                <li>• Date format: YYYY-MM-DD (e.g., 2024-01-15)</li>
                <li>• Amount: Decimal number (e.g., 5.99, 12.00)</li>
                <li>• No currency symbols in amount column</li>
                <li>• Customer ID can be any text identifier</li>
                <li>• Category helps with product grouping</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}