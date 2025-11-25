import { useState } from 'react'

export const DebugAPI = () => {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const testAPI = async () => {
    setLoading(true)
    try {
      console.log('Testing API...')
      
      // Test 1: Direct fetch
      const response = await fetch('http://localhost:8000/api/v1/dashboard/kpis?days=30')
      console.log('Response status:', response.status)
      console.log('Response headers:', [...response.headers.entries()])
      
      const data = await response.json()
      console.log('Response data:', data)
      
      setResult({
        success: true,
        status: response.status,
        data: data
      })
    } catch (error) {
      console.error('API Test Error:', error)
      setResult({
        success: false,
        error: error.message,
        stack: error.stack
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6 bg-white rounded-lg shadow border max-w-2xl mx-auto">
      <h2 className="text-xl font-bold mb-4">API Debug Tool</h2>
      
      <button 
        onClick={testAPI}
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? 'Testing...' : 'Test API Connection'}
      </button>

      {result && (
        <div className="mt-6">
          <h3 className="font-semibold mb-2">Result:</h3>
          <pre className="bg-gray-100 p-4 rounded text-sm overflow-auto max-h-96">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}