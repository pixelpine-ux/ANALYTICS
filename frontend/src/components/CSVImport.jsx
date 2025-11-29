import { useState, useRef } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Download, Database } from 'lucide-react';

function CSVImport({ onImportComplete }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [importType, setImportType] = useState('sales');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const importTypes = [
    { id: 'sales', label: 'Sales Data', icon: Database, description: 'Import sales transactions' },
    { id: 'customers', label: 'Customers', icon: FileText, description: 'Import customer information' },
    { id: 'expenses', label: 'Expenses', icon: FileText, description: 'Import expense records' }
  ];

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      handleFileSelect(files[0]);
    }
  };

  const handleFileSelect = (file) => {
    if (!file.name.endsWith('.csv')) {
      setUploadResult({ success: false, message: 'Please select a CSV file' });
      return;
    }
    setSelectedFile(file);
    setUploadResult(null);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch(`/api/v1/data/upload-${importType}-csv`, {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      
      if (response.ok) {
        setUploadResult({ 
          success: true, 
          message: result.message,
          recordsProcessed: result.records_processed,
          errors: result.errors || []
        });
        setSelectedFile(null);
        if (onImportComplete) onImportComplete(result);
      } else {
        setUploadResult({ success: false, message: result.detail || 'Upload failed' });
      }
    } catch (error) {
      setUploadResult({ success: false, message: 'Network error occurred' });
    } finally {
      setIsUploading(false);
    }
  };

  const downloadTemplate = async () => {
    try {
      const response = await fetch(`/api/v1/data/upload-template/${importType}`);
      const template = await response.json();
      
      // Create CSV content
      const headers = template.columns.join(',');
      const example = template.columns.map(col => template.example[col]).join(',');
      const csvContent = `${headers}\n${example}`;
      
      // Download file
      const blob = new Blob([csvContent], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${importType}_template.csv`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Failed to download template:', error);
    }
  };

  return (
    <div className="relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50/50 via-indigo-50/30 to-purple-50/50"></div>
      
      <div className="relative card card-padding border-l-4 border-l-blue-400 hover:border-l-blue-500 transition-all duration-300">
        {/* Header */}
        <div className="flex items-start justify-between mb-6">
          <div className="flex-1 min-w-0 pr-4">
            <div className="flex items-center space-x-2 mb-1">
              <Upload className="w-5 h-5 text-blue-500" />
              <h3 className="text-lg font-bold text-gray-800">
                CSV Import
              </h3>
            </div>
            <p className="text-sm text-gray-600">
              Bulk import your data from CSV files
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
            <span className="text-xs text-gray-500">Ready</span>
          </div>
        </div>

        {/* Import Type Selection */}
        <div className="mb-6">
          <label className="block text-sm font-semibold text-gray-700 mb-3">
            Data Type
          </label>
          <div className="grid grid-cols-1 gap-2">
            {importTypes.map((type) => (
              <button
                key={type.id}
                onClick={() => setImportType(type.id)}
                className={`flex items-center p-3 rounded-lg border-2 transition-all duration-200 ${
                  importType === type.id
                    ? 'border-blue-400 bg-blue-50 text-blue-700'
                    : 'border-gray-200 hover:border-gray-300 text-gray-600'
                }`}
              >
                <type.icon className="w-4 h-4 mr-3" />
                <div className="text-left">
                  <div className="font-medium">{type.label}</div>
                  <div className="text-xs opacity-75">{type.description}</div>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* File Upload Area */}
        <div
          className={`relative border-2 border-dashed rounded-xl p-6 transition-all duration-200 ${
            dragActive
              ? 'border-blue-400 bg-blue-50'
              : selectedFile
              ? 'border-emerald-400 bg-emerald-50'
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            onChange={(e) => handleFileSelect(e.target.files[0])}
            className="sr-only"
          />
          
          <div className="text-center">
            {selectedFile ? (
              <div className="flex items-center justify-center space-x-2">
                <CheckCircle className="w-8 h-8 text-emerald-500" />
                <div>
                  <p className="font-medium text-emerald-700">{selectedFile.name}</p>
                  <p className="text-sm text-emerald-600">
                    {(selectedFile.size / 1024).toFixed(1)} KB
                  </p>
                </div>
              </div>
            ) : (
              <div>
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-lg font-medium text-gray-700 mb-2">
                  Drop CSV file here
                </p>
                <p className="text-sm text-gray-500 mb-4">
                  or click to browse files
                </p>
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="bg-blue-500 text-white px-4 py-2 rounded-lg font-medium hover:bg-blue-600 transition-colors"
                >
                  Choose File
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-between mt-6">
          <button
            onClick={downloadTemplate}
            className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 font-medium"
          >
            <Download className="w-4 h-4" />
            <span>Download Template</span>
          </button>
          
          <button
            onClick={handleUpload}
            disabled={!selectedFile || isUploading}
            className="bg-gradient-to-r from-blue-500 to-indigo-500 text-white px-6 py-2 rounded-lg font-medium hover:from-blue-600 hover:to-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center space-x-2"
          >
            {isUploading ? (
              <>
                <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
                <span>Uploading...</span>
              </>
            ) : (
              <>
                <Upload className="w-4 h-4" />
                <span>Import Data</span>
              </>
            )}
          </button>
        </div>

        {/* Upload Result */}
        {uploadResult && (
          <div className={`mt-4 p-4 rounded-lg ${
            uploadResult.success ? 'bg-emerald-50 border border-emerald-200' : 'bg-red-50 border border-red-200'
          }`}>
            <div className="flex items-start space-x-2">
              {uploadResult.success ? (
                <CheckCircle className="w-5 h-5 text-emerald-600 mt-0.5" />
              ) : (
                <AlertCircle className="w-5 h-5 text-red-600 mt-0.5" />
              )}
              <div className="flex-1">
                <p className={`font-medium ${
                  uploadResult.success ? 'text-emerald-700' : 'text-red-700'
                }`}>
                  {uploadResult.message}
                </p>
                {uploadResult.recordsProcessed && (
                  <p className="text-sm text-emerald-600 mt-1">
                    {uploadResult.recordsProcessed} records processed successfully
                  </p>
                )}
                {uploadResult.errors && uploadResult.errors.length > 0 && (
                  <div className="mt-2">
                    <p className="text-sm text-red-600 font-medium">Errors:</p>
                    <ul className="text-sm text-red-600 mt-1 space-y-1">
                      {uploadResult.errors.slice(0, 3).map((error, index) => (
                        <li key={index}>• {error}</li>
                      ))}
                      {uploadResult.errors.length > 3 && (
                        <li>• ... and {uploadResult.errors.length - 3} more</li>
                      )}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* Corner accent */}
      <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-bl from-blue-100/50 to-transparent rounded-bl-full"></div>
    </div>
  );
}

export default CSVImport;