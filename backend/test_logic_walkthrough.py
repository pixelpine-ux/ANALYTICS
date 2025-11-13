#!/usr/bin/env python3
"""
Backend Logic Walkthrough - Understanding Data Flow and Algorithms
Run this to see how our analytics engine works step by step
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.models.analytics import Sale, Customer, Expense
from app.services.analytics import AnalyticsService
from app.services.data_processor import DataProcessor

# Create in-memory SQLite database for testing
engine = create_engine("sqlite:///:memory:", echo=True)  # echo=True shows SQL queries
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)

def create_sample_data(db):
    """Create realistic sample data to test our algorithms"""
    print("\n=== CREATING SAMPLE DATA ===")
    
    # Sample sales data - realistic retail scenario
    sample_sales = [
        # Week 1 - January 2024
        Sale(date=datetime(2024, 1, 1), product_name="Coffee", amount_cents=599, customer_id="CUST001", category="beverages"),
        Sale(date=datetime(2024, 1, 1), product_name="Sandwich", amount_cents=850, customer_id="CUST002", category="food"),
        Sale(date=datetime(2024, 1, 2), product_name="Coffee", amount_cents=599, customer_id="CUST001", category="beverages"),  # Repeat customer
        Sale(date=datetime(2024, 1, 2), product_name="Pastry", amount_cents=450, customer_id="CUST003", category="food"),
        
        # Week 2
        Sale(date=datetime(2024, 1, 8), product_name="Coffee", amount_cents=599, customer_id="CUST001", category="beverages"),  # Repeat again
        Sale(date=datetime(2024, 1, 8), product_name="Latte", amount_cents=699, customer_id="CUST004", category="beverages"),
        Sale(date=datetime(2024, 1, 9), product_name="Sandwich", amount_cents=850, customer_id="CUST002", category="food"),  # Repeat customer
        
        # Week 3 - Higher volume day
        Sale(date=datetime(2024, 1, 15), product_name="Coffee", amount_cents=599, customer_id="CUST005", category="beverages"),
        Sale(date=datetime(2024, 1, 15), product_name="Coffee", amount_cents=599, customer_id="CUST006", category="beverages"),
        Sale(date=datetime(2024, 1, 15), product_name="Latte", amount_cents=699, customer_id="CUST007", category="beverages"),
    ]
    
    for sale in sample_sales:
        db.add(sale)
    
    db.commit()
    print(f"✅ Created {len(sample_sales)} sales records")
    return sample_sales

def demonstrate_sql_queries(db):
    """Show the actual SQL queries our analytics service generates"""
    print("\n=== SQL QUERIES DEMONSTRATION ===")
    
    # 1. Revenue Calculation Query
    print("\n1. REVENUE CALCULATION:")
    print("   Algorithm: Single SQL aggregation instead of Python loops")
    
    revenue_sql = text("""
        SELECT 
            SUM(amount_cents) as total_cents,
            COUNT(id) as total_sales,
            AVG(amount_cents) as avg_cents
        FROM sales 
        WHERE date >= :start_date AND date <= :end_date
    """)
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 31)
    
    result = db.execute(revenue_sql, {"start_date": start_date, "end_date": end_date}).fetchone()
    print(f"   Raw SQL Result: {result}")
    print(f"   Total Revenue: ${result[0]/100:.2f}")
    print(f"   Total Sales: {result[1]}")
    print(f"   Average Order: ${result[2]/100:.2f}")
    
    # 2. Top Products Query
    print("\n2. TOP PRODUCTS CALCULATION:")
    print("   Algorithm: GROUP BY with ORDER BY - database handles sorting")
    
    top_products_sql = text("""
        SELECT 
            product_name,
            SUM(amount_cents) as total_revenue_cents,
            COUNT(id) as sales_count
        FROM sales 
        WHERE date >= :start_date AND date <= :end_date
        GROUP BY product_name
        ORDER BY total_revenue_cents DESC
        LIMIT 3
    """)
    
    results = db.execute(top_products_sql, {"start_date": start_date, "end_date": end_date}).fetchall()
    print("   Top Products by Revenue:")
    for i, (product, revenue_cents, count) in enumerate(results, 1):
        print(f"   {i}. {product}: ${revenue_cents/100:.2f} ({count} sales)")
    
    # 3. Repeat Customers Query
    print("\n3. REPEAT CUSTOMERS CALCULATION:")
    print("   Algorithm: GROUP BY customer with HAVING count > 1")
    
    repeat_customers_sql = text("""
        SELECT 
            customer_id,
            COUNT(id) as purchase_count
        FROM sales 
        WHERE date >= :start_date AND date <= :end_date
        AND customer_id IS NOT NULL
        GROUP BY customer_id
        HAVING COUNT(id) > 1
    """)
    
    results = db.execute(repeat_customers_sql, {"start_date": start_date, "end_date": end_date}).fetchall()
    print(f"   Repeat Customers Found: {len(results)}")
    for customer_id, count in results:
        print(f"   - {customer_id}: {count} purchases")

def test_analytics_service(db):
    """Test our AnalyticsService with the sample data"""
    print("\n=== ANALYTICS SERVICE TESTING ===")
    
    analytics = AnalyticsService(db)
    
    # Test KPI Summary
    print("\n1. TESTING KPI SUMMARY:")
    kpi_summary = analytics.generate_kpi_summary(days_back=30)
    
    print(f"   📊 Total Revenue: ${kpi_summary['total_revenue']:.2f}")
    print(f"   📈 Total Sales: {kpi_summary['total_sales_count']}")
    print(f"   💰 Average Order Value: ${kpi_summary['average_order_value']:.2f}")
    print(f"   🔄 Repeat Customers: {kpi_summary['repeat_customers_count']}")
    
    print("\n   🏆 Top Products:")
    for i, product in enumerate(kpi_summary['top_products'], 1):
        print(f"   {i}. {product['product_name']}: ${product['total_revenue']:.2f}")
    
    # Test Revenue Trend
    print("\n2. TESTING REVENUE TREND:")
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 31)
    
    trend_data = analytics.get_revenue_trend(start_date, end_date, interval='daily')
    print("   Daily Revenue Trend:")
    for day_data in trend_data[:5]:  # Show first 5 days
        print(f"   {day_data['period']}: ${day_data['revenue']:.2f}")

def test_data_processor(db):
    """Test CSV processing logic"""
    print("\n=== DATA PROCESSOR TESTING ===")
    
    # Sample CSV content
    csv_content = """date,product_name,amount,customer_id,category
2024-01-20,Espresso,4.99,CUST008,beverages
2024-01-20,Croissant,3.50,CUST009,food
2024-01-21,Invalid Amount,abc,CUST010,food
2024-01-21,Cappuccino,5.99,CUST008,beverages"""
    
    processor = DataProcessor(db)
    records_processed, errors = processor.process_csv_content(csv_content)
    
    print(f"   📁 CSV Processing Results:")
    print(f"   ✅ Records Processed: {records_processed}")
    print(f"   ❌ Errors Found: {len(errors)}")
    
    if errors:
        print("   Error Details:")
        for error in errors:
            print(f"   - {error}")

def demonstrate_performance_concepts():
    """Explain the performance optimizations we implemented"""
    print("\n=== PERFORMANCE CONCEPTS EXPLAINED ===")
    
    print("\n1. 🚀 DATABASE INDEXING:")
    print("   - Index on 'date' column → Fast time-range queries")
    print("   - Index on 'customer_id' → Fast repeat customer analysis")
    print("   - Composite index on (date, customer_id) → Optimized for both")
    
    print("\n2. 💾 MEMORY EFFICIENCY:")
    print("   - Store money as integers (cents) → No floating-point errors")
    print("   - Batch processing for CSV uploads → Handle large files")
    print("   - SQL aggregation instead of Python loops → Database optimization")
    
    print("\n3. 🔄 ALGORITHM CHOICES:")
    print("   - Dictionary/HashMap for lookups → O(1) access time")
    print("   - SQL GROUP BY for aggregations → Optimized by database engine")
    print("   - Single-pass processing → Minimize data scanning")

def main():
    """Run the complete walkthrough"""
    print("🎯 RETAIL ANALYTICS BACKEND - LOGIC WALKTHROUGH")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Step 1: Create sample data
        sample_sales = create_sample_data(db)
        
        # Step 2: Show SQL queries in action
        demonstrate_sql_queries(db)
        
        # Step 3: Test analytics service
        test_analytics_service(db)
        
        # Step 4: Test data processing
        test_data_processor(db)
        
        # Step 5: Explain performance concepts
        demonstrate_performance_concepts()
        
        print("\n" + "=" * 60)
        print("✅ WALKTHROUGH COMPLETE - Backend logic verified!")
        print("🎓 Key Learning: SQL does heavy lifting, Python orchestrates")
        
    finally:
        db.close()

if __name__ == "__main__":
    main()