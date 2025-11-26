import { useState } from 'react'
import { FileUpload } from '../components/forms/FileUpload'
import { useToast } from '../components/ui/Toast'
import { ErrorBoundary } from '../components/ui/ErrorBoundary'

export const Upload = () => {
  const [uploadSuccess, setUploadSuccess] = useState(false)
  const { showToast, ToastContainer } = useToast()

  const handleUploadSuccess = (result) => {
    setUploadSuccess(true)
    showToast(`Successfully uploaded ${result.records_processed} records!`)
    // Auto-redirect to dashboard after 3 seconds
    setTimeout(() => {
      window.location.href = '/'
    }, 3000)
  }

  const handleUploadError = (error) => {
    showToast(`Upload failed: ${error}`, 'error')
  }

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <ToastContainer />
        
        {/* Header */}
        <div className="bg-white/90 backdrop-blur-md border-b border-slate-200/60 shadow-sm">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center shadow-lg">
                <span className="text-white text-xl">📄</span>
              </div>
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
                  Upload Data
                </h1>
                <p className="mt-2 text-slate-600 flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-2 animate-pulse"></span>
                  Import your sales data to generate analytics insights
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <ErrorBoundary>
            <FileUpload onSuccess={handleUploadSuccess} onError={handleUploadError} />
          </ErrorBoundary>

          {uploadSuccess && (
            <div className="mt-8 text-center animate-fade-in">
              <div className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-emerald-50 to-emerald-100 border border-emerald-200 text-emerald-800 rounded-xl shadow-lg">
                <span className="text-2xl mr-3 animate-bounce">🎉</span>
                <div>
                  <div className="font-semibold text-lg">Upload Successful!</div>
                  <div className="text-sm opacity-80">Redirecting to dashboard...</div>
                </div>
              </div>
            </div>
          )}

          {/* CSV Format Guide */}
          <div className="mt-12 bg-white rounded-xl shadow-card border border-slate-200 hover:shadow-soft transition-all duration-200">
            <div className="px-6 py-5 border-b border-slate-200">
              <h2 className="text-xl font-semibold text-slate-900 flex items-center">
                <span className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center text-white text-sm mr-3">
                  📊
                </span>
                CSV Format Requirements
              </h2>
            </div>
            <div className="p-6">
              <div className="grid md:grid-cols-2 gap-6">
                {/* Required Format */}
                <div className="group">
                  <h3 className="font-semibold text-slate-900 mb-3 flex items-center">
                    <span className="w-6 h-6 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center text-xs mr-2">✓</span>
                    Required Columns
                  </h3>
                  <div className="bg-slate-50 p-4 rounded-lg font-mono text-sm border border-slate-200 group-hover:border-slate-300 transition-colors">
                    <div className="text-slate-600 mb-2 font-medium">Header row:</div>
                    <div className="font-bold text-slate-900 bg-white px-2 py-1 rounded border">date,product_name,amount</div>
                    
                    <div className="text-slate-600 mt-4 mb-2 font-medium">Example data:</div>
                    <div className="space-y-1 bg-white p-2 rounded border">
                      <div className="text-slate-700">2024-01-15,Coffee,5.99</div>
                      <div className="text-slate-700">2024-01-16,Sandwich,8.50</div>
                      <div className="text-slate-700">2024-01-17,Salad,12.00</div>
                    </div>
                  </div>
                </div>

                {/* Optional Format */}
                <div className="group">
                  <h3 className="font-semibold text-slate-900 mb-3 flex items-center">
                    <span className="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs mr-2">+</span>
                    With Optional Columns
                  </h3>
                  <div className="bg-slate-50 p-4 rounded-lg font-mono text-sm border border-slate-200 group-hover:border-slate-300 transition-colors">
                    <div className="text-slate-600 mb-2 font-medium">Full format:</div>
                    <div className="font-bold text-slate-900 text-xs bg-white px-2 py-1 rounded border break-all">date,product_name,amount,customer_id,category</div>
                    
                    <div className="text-slate-600 mt-4 mb-2 font-medium">Example data:</div>
                    <div className="space-y-1 text-xs bg-white p-2 rounded border">
                      <div className="text-slate-700">2024-01-15,Coffee,5.99,CUST001,beverages</div>
                      <div className="text-slate-700">2024-01-16,Sandwich,8.50,CUST002,food</div>
                      <div className="text-slate-700">2024-01-17,Salad,12.00,CUST001,food</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Format Notes */}
              <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-200">
                <h4 className="font-semibold text-blue-900 mb-4 flex items-center">
                  <span className="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs mr-2">i</span>
                  Format Notes
                </h4>
                <div className="grid md:grid-cols-2 gap-4">
                  <ul className="text-sm text-blue-800 space-y-2">
                    <li className="flex items-start">
                      <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Date format: YYYY-MM-DD (e.g., 2024-01-15)</span>
                    </li>
                    <li className="flex items-start">
                      <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Amount: Decimal number (e.g., 5.99, 12.00)</span>
                    </li>
                    <li className="flex items-start">
                      <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>No currency symbols in amount column</span>
                    </li>
                  </ul>
                  <ul className="text-sm text-blue-800 space-y-2">
                    <li className="flex items-start">
                      <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Customer ID can be any text identifier</span>
                    </li>
                    <li className="flex items-start">
                      <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                      <span>Category helps with product grouping</span>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ErrorBoundary>
  )
}