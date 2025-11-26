import { useState, useCallback } from 'react'
import { LoadingSpinner } from '../ui/LoadingSpinner'

export const FileUpload = ({ onSuccess, onError }) => {
  const [dragActive, setDragActive] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState(null)
  const [uploadProgress, setUploadProgress] = useState(0)

  const uploadFile = async (file) => {
    setUploading(true)
    setResult(null)
    setUploadProgress(0)

    try {
      // Simulate progress for better UX
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => Math.min(prev + 10, 90))
      }, 200)

      const formData = new FormData()
      formData.append('file', file)
      
      const response = await fetch('http://127.0.0.1:8000/api/v1/data/upload-sales-csv', {
        method: 'POST',
        body: formData
      })
      
      clearInterval(progressInterval)
      setUploadProgress(100)
      
      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status}`)
      }
      
      const data = await response.json()
      setResult(data)
      onSuccess?.(data)
    } catch (error) {
      const errorMsg = error.message
      setResult({ error: errorMsg })
      onError?.(errorMsg)
    } finally {
      setUploading(false)
      setTimeout(() => setUploadProgress(0), 1000)
    }
  }

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setDragActive(false)
    
    const files = Array.from(e.dataTransfer.files)
    const csvFile = files.find(file => file.name.endsWith('.csv'))
    
    if (csvFile) {
      uploadFile(csvFile)
    } else {
      setResult({ error: 'Please upload a CSV file' })
    }
  }, [])

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) uploadFile(file)
  }

  return (
    <div className="max-w-2xl mx-auto">
      {/* Upload Zone */}
      <div
        className={`
          border-2 border-dashed rounded-xl p-12 text-center transition-all cursor-pointer group
          ${dragActive ? 'border-primary-400 bg-primary-50 scale-105' : 'border-slate-300 hover:border-primary-400 hover:bg-primary-50/30'}
          ${uploading ? 'opacity-50 pointer-events-none' : ''}
        `}
        onDrop={handleDrop}
        onDragOver={(e) => e.preventDefault()}
        onDragEnter={() => setDragActive(true)}
        onDragLeave={() => setDragActive(false)}
        onClick={() => document.getElementById('file-input').click()}
      >
        <input
          id="file-input"
          type="file"
          accept=".csv"
          onChange={handleFileSelect}
          className="hidden"
        />
        
        {uploading ? (
          <div className="animate-fade-in">
            <div className="relative w-16 h-16 mx-auto mb-6">
              <LoadingSpinner size="xl" className="absolute inset-0" />
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-xs font-bold text-primary-600">{uploadProgress}%</span>
              </div>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2 mb-4">
              <div 
                className="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
            <p className="text-slate-700 font-semibold text-lg">Processing your data...</p>
            <p className="text-sm text-slate-500 mt-2">Analyzing {uploadProgress < 50 ? 'file structure' : uploadProgress < 80 ? 'data validation' : 'finalizing import'}</p>
          </div>
        ) : (
          <div className="group-hover:scale-105 transition-transform duration-200">
            <div className="text-6xl mb-6 animate-bounce-in">📊</div>
            <h3 className="text-2xl font-bold text-slate-900 mb-3">
              Upload Sales Data
            </h3>
            <p className="text-slate-600 mb-6 text-lg">
              Drag and drop your CSV file here, or click to browse
            </p>
            <div className="bg-slate-50 rounded-lg p-4 text-sm text-slate-600 border border-slate-200">
              <div className="flex items-center justify-center space-x-4 mb-2">
                <span className="flex items-center">
                  <span className="w-2 h-2 bg-emerald-500 rounded-full mr-2"></span>
                  Required: <code className="ml-1 bg-white px-2 py-1 rounded text-xs">date, product_name, amount</code>
                </span>
              </div>
              <div className="flex items-center justify-center">
                <span className="flex items-center">
                  <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                  Optional: <code className="ml-1 bg-white px-2 py-1 rounded text-xs">customer_id, category</code>
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Result Display */}
      {result && (
        <div className={`mt-8 p-6 rounded-xl border animate-slide-up ${
          result.error 
            ? 'bg-red-50 border-red-200 shadow-red-100' 
            : 'bg-emerald-50 border-emerald-200 shadow-emerald-100'
        } shadow-lg`}>
          {result.error ? (
            <div>
              <div className="flex items-center mb-3">
                <div className="w-10 h-10 bg-red-100 rounded-full flex items-center justify-center mr-3">
                  <span className="text-red-600 text-xl">❌</span>
                </div>
                <div>
                  <h4 className="font-bold text-red-800 text-lg">Upload Failed</h4>
                  <p className="text-red-600 text-sm">Please check your file and try again</p>
                </div>
              </div>
              <div className="bg-red-100 rounded-lg p-4 border border-red-200">
                <p className="text-red-800 font-medium">{result.error}</p>
              </div>
            </div>
          ) : (
            <div>
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-emerald-100 rounded-full flex items-center justify-center mr-4">
                  <span className="text-emerald-600 text-2xl">✅</span>
                </div>
                <div>
                  <h4 className="font-bold text-emerald-800 text-xl">Upload Successful!</h4>
                  <p className="text-emerald-600">Your data has been imported</p>
                </div>
              </div>
              <div className="bg-emerald-100 rounded-lg p-4 border border-emerald-200 mb-4">
                <p className="text-emerald-800 font-semibold text-lg">
                  📈 Processed {result.records_processed} records successfully
                </p>
              </div>
              
              {result.errors?.length > 0 && (
                <details className="bg-amber-50 border border-amber-200 rounded-lg p-4">
                  <summary className="cursor-pointer font-semibold text-amber-800 hover:text-amber-900 flex items-center">
                    <span className="w-5 h-5 bg-amber-100 rounded-full flex items-center justify-center mr-2 text-xs">⚠️</span>
                    View {result.errors.length} warnings
                  </summary>
                  <div className="mt-3 pl-4 border-l-4 border-amber-300 bg-amber-25">
                    {result.errors.slice(0, 5).map((error, i) => (
                      <p key={i} className="text-sm text-amber-700 mb-2 flex items-start">
                        <span className="w-1.5 h-1.5 bg-amber-500 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                        {error}
                      </p>
                    ))}
                    {result.errors.length > 5 && (
                      <p className="text-sm text-amber-600 font-medium">
                        📝 ... and {result.errors.length - 5} more warnings
                      </p>
                    )}
                  </div>
                </details>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}