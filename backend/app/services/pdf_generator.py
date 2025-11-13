from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import base64
from sqlalchemy.orm import Session
from .analytics import AnalyticsService


class PDFReportGenerator:
    """
    PDF report generation using HTML templates
    Senior Engineer Principle: Use simple, reliable tools that work everywhere
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.analytics = AnalyticsService(db)
    
    def generate_kpi_report(self, days_back: int = 30, business_name: str = "Your Business") -> bytes:
        """
        Generate comprehensive KPI report as PDF
        
        Algorithm: HTML template → PDF conversion
        Why HTML first: Easier to style, test, and maintain than direct PDF generation
        """
        try:
            # Get analytics data
            kpi_data = self.analytics.generate_kpi_summary(days_back)
            
            # Generate trend data for chart
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days_back)
            trend_data = self.analytics.get_revenue_trend(start_date, end_date, interval='daily')
            
            # Create HTML report
            html_content = self._generate_html_report(kpi_data, trend_data, business_name, days_back)
            
            # Convert to PDF
            pdf_bytes = self._html_to_pdf(html_content)
            
            return pdf_bytes
            
        except Exception as e:
            raise RuntimeError(f"PDF generation failed: {str(e)}")
    
    def _generate_html_report(self, kpi_data: Dict, trend_data: List[Dict], 
                            business_name: str, days_back: int) -> str:
        """
        Generate HTML report template
        Algorithm: String templating with embedded CSS for consistent styling
        """
        
        # Prepare chart data for JavaScript
        chart_labels = [item['period'] for item in trend_data[-14:]]  # Last 14 days
        chart_values = [item['revenue'] for item in trend_data[-14:]]
        
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Analytics Report - {business_name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 40px;
            color: #333;
            line-height: 1.6;
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #2563eb;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #1e40af;
            margin: 0;
            font-size: 28px;
        }}
        .period {{
            color: #6b7280;
            font-size: 14px;
            margin-top: 5px;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        .kpi-card {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }}
        .kpi-value {{
            font-size: 32px;
            font-weight: bold;
            color: #059669;
            margin: 10px 0;
        }}
        .kpi-label {{
            color: #6b7280;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section h2 {{
            color: #1e40af;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 10px;
        }}
        .products-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        .products-table th,
        .products-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }}
        .products-table th {{
            background-color: #f1f5f9;
            font-weight: 600;
            color: #374151;
        }}
        .chart-container {{
            background: #f8fafc;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            color: #6b7280;
            font-size: 12px;
            border-top: 1px solid #e2e8f0;
            padding-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{business_name}</h1>
        <h2>Analytics Report</h2>
        <div class="period">
            Period: {kpi_data['period_start'].strftime('%B %d, %Y')} - {kpi_data['period_end'].strftime('%B %d, %Y')}
            ({days_back} days)
        </div>
    </div>

    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">${kpi_data['total_revenue']:,.2f}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Total Sales</div>
            <div class="kpi-value">{kpi_data['total_sales_count']:,}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Average Order Value</div>
            <div class="kpi-value">${kpi_data['average_order_value']:,.2f}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Repeat Customers</div>
            <div class="kpi-value">{kpi_data['repeat_customers_count']}</div>
        </div>
    </div>

    <div class="section">
        <h2>Top Products by Revenue</h2>
        <table class="products-table">
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Product Name</th>
                    <th>Revenue</th>
                    <th>Sales Count</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Add top products to table
        for i, product in enumerate(kpi_data['top_products'][:5], 1):
            html_template += f"""
                <tr>
                    <td>{i}</td>
                    <td>{product['product_name']}</td>
                    <td>${product['total_revenue']:,.2f}</td>
                    <td>{product['sales_count']}</td>
                </tr>
"""
        
        html_template += f"""
            </tbody>
        </table>
    </div>

    <div class="section">
        <h2>Revenue Trend (Last 14 Days)</h2>
        <div class="chart-container">
            <canvas id="revenueChart" width="600" height="300"></canvas>
        </div>
    </div>

    <div class="footer">
        <p>Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        <p>Retail Analytics Dashboard - Automated Report</p>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        const ctx = document.getElementById('revenueChart').getContext('2d');
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(chart_labels)},
                datasets: [{{
                    label: 'Daily Revenue',
                    data: {json.dumps(chart_values)},
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    borderWidth: 2,
                    fill: true
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value.toFixed(2);
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
        
        return html_template
    
    def _html_to_pdf(self, html_content: str) -> bytes:
        """
        Convert HTML to PDF using available tools
        
        Algorithm: Try multiple PDF generation methods for reliability
        1. WeasyPrint (CSS support, good for reports)
        2. Playwright (headless browser, handles JavaScript)
        3. Fallback to simple HTML file
        """
        
        # Method 1: Try WeasyPrint (best for static HTML/CSS)
        try:
            from weasyprint import HTML, CSS
            from io import BytesIO
            
            pdf_buffer = BytesIO()
            HTML(string=html_content).write_pdf(pdf_buffer)
            return pdf_buffer.getvalue()
            
        except ImportError:
            pass  # WeasyPrint not installed
        except Exception as e:
            print(f"WeasyPrint failed: {e}")
        
        # Method 2: Try Playwright (handles JavaScript charts)
        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.set_content(html_content)
                
                # Wait for chart to render
                page.wait_for_timeout(2000)
                
                pdf_bytes = page.pdf(
                    format='A4',
                    margin={'top': '1in', 'right': '1in', 'bottom': '1in', 'left': '1in'}
                )
                
                browser.close()
                return pdf_bytes
                
        except ImportError:
            pass  # Playwright not installed
        except Exception as e:
            print(f"Playwright failed: {e}")
        
        # Fallback: Return HTML as bytes (can be saved as .html file)
        return html_content.encode('utf-8')
    
    def generate_public_report_link(self, days_back: int = 30, 
                                  business_name: str = "Your Business") -> str:
        """
        Generate a public shareable link for the report
        
        Algorithm: Create static HTML file with unique ID
        Security: No sensitive data, read-only access
        """
        try:
            # Generate unique report ID
            import hashlib
            import time
            
            report_id = hashlib.md5(f"{business_name}{time.time()}".encode()).hexdigest()[:12]
            
            # Get report data
            kpi_data = self.analytics.generate_kpi_summary(days_back)
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days_back)
            trend_data = self.analytics.get_revenue_trend(start_date, end_date, interval='daily')
            
            # Generate HTML
            html_content = self._generate_html_report(kpi_data, trend_data, business_name, days_back)
            
            # In production, save to cloud storage or static file server
            # For now, return the report ID and content
            return {
                "report_id": report_id,
                "public_url": f"/public/reports/{report_id}",
                "html_content": html_content,
                "expires_at": (datetime.utcnow() + timedelta(days=7)).isoformat()
            }
            
        except Exception as e:
            raise RuntimeError(f"Public report generation failed: {str(e)}")