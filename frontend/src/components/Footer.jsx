import { Heart, Shield, Zap, TrendingUp, Twitter, Github, Linkedin } from 'lucide-react';

function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gradient-to-r from-gray-900 to-blue-900 text-white">
      <div className="max-w-7xl mx-auto px-4 py-12 md:py-16">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Section */}
          <div className="md:col-span-2">
            <div className="flex items-center mb-4">
              <TrendingUp className="w-8 h-8 text-amber-400 mr-3" />
              <h3 className="text-xl font-bold">Retail Analytics</h3>
            </div>
            <p className="text-gray-300 mb-4 leading-relaxed">
              Empowering small retail businesses with real-time analytics, 
              smart insights, and future-ready marketing automation.
            </p>
            <div className="flex items-center space-x-6 text-sm text-gray-400">
              <div className="flex items-center">
                <Shield className="w-4 h-4 mr-2" />
                <span>Secure & Private</span>
              </div>
              <div className="flex items-center">
                <Zap className="w-4 h-4 mr-2" />
                <span>Real-time Updates</span>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Features</h4>
            <ul className="space-y-2 text-gray-300">
              <li>Dashboard Analytics</li>
              <li>Sales Tracking</li>
              <li>Customer Insights</li>
              <li>CSV Data Import</li>
              <li>Performance Reports</li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Support</h4>
            <ul className="space-y-2 text-gray-300">
              <li>Documentation</li>
              <li>API Reference</li>
              <li>Setup Guide</li>
              <li>Best Practices</li>
              <li>Community</li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center text-gray-400 mb-4 md:mb-0">
            <span>Built with</span>
            <Heart className="w-4 h-4 mx-2 text-red-400" />
            <span>for small retail businesses</span>
          </div>
          <div className="flex items-center space-x-4">
            <a href="#" className="text-gray-400 hover:text-white">
              <Twitter className="w-5 h-5" />
            </a>
            <a href="#" className="text-gray-400 hover:text-white">
              <Github className="w-5 h-5" />
            </a>
            <a href="#" className="text-gray-400 hover:text-white">
              <Linkedin className="w-5 h-5" />
            </a>
          </div>
          <div className="text-gray-400 text-sm">
            © {currentYear} Retail Analytics. Open Source MIT License.
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;