import { useState, useRef, useEffect } from 'react';
import { Plus, DollarSign, Package, CheckCircle, AlertCircle, Zap, TrendingUp } from 'lucide-react';

function SaleForm({ onSaleAdded, isSubmitting = false }) {
  const [formData, setFormData] = useState({
    product: '',
    amount: ''
  });
  const [errors, setErrors] = useState({});
  const [showSuccess, setShowSuccess] = useState(false);
  
  // Refs for accessibility
  const formRef = useRef(null);
  const productInputRef = useRef(null);
  const amountInputRef = useRef(null);
  const errorAnnouncementRef = useRef(null);
  
  // Announce errors to screen readers
  useEffect(() => {
    if (Object.keys(errors).length > 0 && errorAnnouncementRef.current) {
      const errorMessages = Object.values(errors).join('. ');
      errorAnnouncementRef.current.textContent = `Form errors: ${errorMessages}`;
    }
  }, [errors]);

  // Form validation
  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.product.trim()) {
      newErrors.product = 'Product name is required';
    }
    
    if (!formData.amount || parseFloat(formData.amount) <= 0) {
      newErrors.amount = 'Amount must be greater than 0';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    try {
      await onSaleAdded({
        product_name: formData.product.trim(),
        amount: parseFloat(formData.amount)
      });

      // Reset form and show success
      setFormData({ product: '', amount: '' });
      setErrors({});
      setShowSuccess(true);
      
      // Focus back to first input for better UX
      setTimeout(() => {
        productInputRef.current?.focus();
      }, 100);
      
      // Hide success message after 3 seconds
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error) {
      setErrors({ submit: 'Failed to add sale. Please try again.' });
      // Focus on first error field
      setTimeout(() => {
        const firstErrorField = formRef.current?.querySelector('[aria-invalid="true"]');
        firstErrorField?.focus();
      }, 100);
    }
  };

  // Handle input changes
  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  return (
    <div className="relative overflow-hidden">
      {/* Animated background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-white via-amber-50/30 to-orange-50/30 opacity-60"></div>
      
      {/* Main card with enhanced styling */}
      <div className="relative card card-padding-sm border-l-4 border-l-amber-400 hover:border-l-amber-500 transition-all duration-300 hover:shadow-xl">
        {/* Screen reader announcements */}
        <div 
          ref={errorAnnouncementRef}
          className="sr-only" 
          aria-live="assertive" 
          aria-atomic="true"
        ></div>
      
      {/* Modern Header with Gradient */}
      <div className="relative mb-4">
        <div className="flex items-center space-x-2 mb-1">
          <Zap className="w-4 h-4 text-amber-500" aria-hidden="true" />
          <h3 
            className="text-base font-bold text-gray-800"
            id="sale-form-title"
          >
            Quick Sale
          </h3>
        </div>
      </div>

      {/* Success Message */}
      {showSuccess && (
        <div 
          className="mb-4 p-3 bg-emerald-50 border border-emerald-200 rounded-lg flex items-center"
          role="status"
          aria-live="polite"
          aria-label="Success message"
        >
          <CheckCircle className="w-4 h-4 text-emerald-600 mr-2" aria-hidden="true" />
          <span className="text-sm text-emerald-700 font-medium">
            Sale added successfully!
          </span>
        </div>
      )}

      {/* Error Message */}
      {errors.submit && (
        <div 
          className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center"
          role="alert"
          aria-live="assertive"
        >
          <AlertCircle className="w-4 h-4 text-red-600 mr-2" aria-hidden="true" />
          <span className="text-sm text-red-700 font-medium">
            {errors.submit}
          </span>
        </div>
      )}

      <form 
        ref={formRef}
        onSubmit={handleSubmit} 
        className="component-spacing-sm"
        aria-labelledby="sale-form-title"
        aria-describedby="sale-form-description"
        noValidate
      >
        {/* Enhanced Product Name Field */}
        <div className="group">
          <label 
            htmlFor="product-input"
            className="block text-sm font-semibold text-gray-700 mb-3"
          >
            Product Name *
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Package 
                className={`w-5 h-5 transition-colors ${
                  errors.product ? 'text-red-400' : 'text-gray-400 group-focus-within:text-amber-500'
                }`}
                aria-hidden="true"
              />
            </div>
            <input
              ref={productInputRef}
              id="product-input"
              type="text"
              placeholder="e.g., iPhone 15 Pro, MacBook Air..."
              value={formData.product}
              onChange={(e) => handleChange('product', e.target.value)}
              className={`w-full pl-12 pr-4 py-4 border-2 rounded-xl font-medium transition-all duration-200 ${
                errors.product 
                  ? 'border-red-300 focus:ring-red-200 bg-red-50 focus:border-red-400' 
                  : 'border-gray-200 focus:ring-amber-200 focus:border-amber-400 hover:border-gray-300'
              } focus:outline-none focus:ring-4`}
              disabled={isSubmitting}
              required
              aria-invalid={errors.product ? 'true' : 'false'}
              aria-describedby={errors.product ? 'product-error' : undefined}
            />
            {/* Success indicator */}
            {formData.product && !errors.product && (
              <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <CheckCircle className="w-5 h-5 text-emerald-500" aria-hidden="true" />
              </div>
            )}
          </div>
          {errors.product && (
            <p 
              id="product-error"
              className="mt-2 text-sm text-red-600 flex items-center animate-in slide-in-from-top-1 duration-200"
              role="alert"
            >
              <AlertCircle className="w-4 h-4 mr-2" aria-hidden="true" />
              {errors.product}
            </p>
          )}
        </div>

        {/* Enhanced Amount Field */}
        <div className="group">
          <label 
            htmlFor="amount-input"
            className="block text-sm font-semibold text-gray-700 mb-3"
          >
            Sale Amount *
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <DollarSign 
                className={`w-5 h-5 transition-colors ${
                  errors.amount ? 'text-red-400' : 'text-gray-400 group-focus-within:text-amber-500'
                }`}
                aria-hidden="true"
              />
            </div>
            <input
              ref={amountInputRef}
              id="amount-input"
              type="number"
              step="0.01"
              min="0.01"
              placeholder="0.00"
              value={formData.amount}
              onChange={(e) => handleChange('amount', e.target.value)}
              className={`w-full pl-12 pr-4 py-4 border-2 rounded-xl font-bold text-lg transition-all duration-200 ${
                errors.amount 
                  ? 'border-red-300 focus:ring-red-200 bg-red-50 focus:border-red-400' 
                  : 'border-gray-200 focus:ring-amber-200 focus:border-amber-400 hover:border-gray-300'
              } focus:outline-none focus:ring-4`}
              disabled={isSubmitting}
              required
              aria-invalid={errors.amount ? 'true' : 'false'}
              aria-describedby={errors.amount ? 'amount-error' : 'amount-help'}
            />
            {/* Success indicator */}
            {formData.amount && !errors.amount && parseFloat(formData.amount) > 0 && (
              <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                <CheckCircle className="w-5 h-5 text-emerald-500" aria-hidden="true" />
              </div>
            )}
          </div>
          <p id="amount-help" className="mt-2 text-xs text-gray-500 flex items-center">
            <TrendingUp className="w-3 h-3 mr-1" aria-hidden="true" />
            Enter amount in USD (e.g., 1299.99)
          </p>
          {errors.amount && (
            <p 
              id="amount-error"
              className="mt-2 text-sm text-red-600 flex items-center animate-in slide-in-from-top-1 duration-200"
              role="alert"
            >
              <AlertCircle className="w-4 h-4 mr-2" aria-hidden="true" />
              {errors.amount}
            </p>
          )}
        </div>

        {/* Enhanced Submit Button */}
        <div className="pt-2">
          <button
            type="submit"
            disabled={isSubmitting || !formData.product || !formData.amount}
            className="group relative w-full bg-gradient-to-r from-amber-400 to-orange-400 text-white py-4 px-6 rounded-xl font-bold text-lg shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-amber-200 hover:scale-[1.02] active:scale-[0.98]"
            aria-describedby="submit-help"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-amber-500 to-orange-500 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <div className="relative flex items-center justify-center">
              {isSubmitting ? (
                <>
                  <div 
                    className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full mr-3"
                    aria-hidden="true"
                  ></div>
                  <span>Processing Sale...</span>
                  <span className="sr-only">Please wait, processing your sale</span>
                </>
              ) : (
                <>
                  <Zap className="w-5 h-5 mr-2" aria-hidden="true" />
                  <span>Record Sale</span>
                </>
              )}
            </div>
          </button>
          
          {/* Quick Stats Below Button */}
          <div className="mt-4 grid grid-cols-2 gap-3 text-center">
            <div className="bg-gray-50 rounded-lg p-2">
              <div className="text-lg font-bold text-gray-800">$2,847</div>
              <div className="text-xs text-gray-500">Today</div>
            </div>
            <div className="bg-gray-50 rounded-lg p-2">
              <div className="text-lg font-bold text-gray-800">12</div>
              <div className="text-xs text-gray-500">Sales</div>
            </div>
          </div>
          
          <p id="submit-help" className="text-xs text-gray-400 text-center mt-3">
            ⚡ Instant processing • 🔒 Secure
          </p>
        </div>
      </form>
      </div>
      
      {/* Subtle corner accent */}
      <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-bl from-amber-100/50 to-transparent rounded-bl-full"></div>
    </div>
  );
}

export default SaleForm;