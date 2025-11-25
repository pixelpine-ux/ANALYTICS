import { useState, useCallback } from 'react'
import { uploadAPI } from '../../services/api'

export const FileUpload = ({ onSuccess }) => {
  const [dragActive, setDragActive] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState(null)

  const uploadFile = async (file) => {
    setUploading(true)
    setResult(null)

    try {
      const data = await uploadAPI.uploadSalesCSV(file)
      setResult(data)
      onSuccess?.(data)
    } catch (error) {
      setResult({ error: error.message })
    } finally {
      setUploading(false)
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
          <div>
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
            <p className="text-gray-600 font-medium">Processing your data...</p>
            <p className="text-sm text-gray-500 mt-1">This may take a few moments</p>
          </div>
        ) : (
          <div>
            <div className="text-5xl mb-4">📊</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Upload Sales Data
            </h3>
            <p className="text-gray-600 mb-4">
              Drag and drop your CSV file here, or click to browse
            </p>
            <div className="text-sm text-gray-500 space-y-1">
              <p>Required columns: <span className="font-mono">date, product_name, amount</span></p>
              <p>Optional columns: <span className="font-mono">customer_id, category</span></p>
            </div>
          </div>
        )}
      </div>

      {/* Result Display */}
      {result && (
        <div className={`mt-6 p-4 rounded-lg border ${
          result.error 
            ? 'bg-red-50 border-red-200' 
            : 'bg-success-50 border-success-200'
        }`}>
          {result.error ? (
            <div>
              <div className="flex items-center mb-2">
                <span className="text-red-600 text-xl mr-2">❌</span>
                <h4 className="font-semibold text-red-800">Upload Failed</h4>
              </div>
              <p className="text-red-700">{result.error}</p>
            </div>
          ) : (
            <div>
              <div className="flex items-center mb-2">
                <span className="text-success-600 text-xl mr-2">✅</span>
                <h4 className="font-semibold text-success-800">Upload Successful!</h4>
              </div>
              <p className="text-success-700 mb-2">
                Processed {result.records_processed} records successfully
              </p>
              
              {result.errors?.length > 0 && (
                <details className="mt-3">
                  <summary className="cursor-pointer text-sm font-medium text-success-800 hover:text-success-900">
                    View {result.errors.length} warnings
                  </summary>
                  <div className="mt-2 pl-4 border-l-2 border-success-300">
                    {result.errors.slice(0, 5).map((error, i) => (
                      <p key={i} className="text-sm text-success-700 mb-1">• {error}</p>
                    ))}
                    {result.errors.length > 5 && (
                      <p className="text-sm text-success-600">
                        ... and {result.errors.length - 5} more
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