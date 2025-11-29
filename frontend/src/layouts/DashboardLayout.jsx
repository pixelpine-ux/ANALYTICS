import Header from '../components/Header';
import Navigation from '../components/Navigation';
import Footer from '../components/Footer';

function DashboardLayout({ children, lastUpdated, onRefresh, isLoading }) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header
        lastUpdated={lastUpdated}
        onRefresh={onRefresh}
        isLoading={isLoading}
      />
      <Navigation />
      <main className="section-spacing">
        <div className="container-main">
          {children}
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default DashboardLayout;