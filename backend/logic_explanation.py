#!/usr/bin/env python3
"""
Backend Logic Explanation - No Dependencies Required
Understanding our analytics algorithms and data structures
"""

def demonstrate_revenue_calculation():
    """Show how revenue calculation works with sample data"""
    print("=== REVENUE CALCULATION ALGORITHM ===")
    
    # Sample sales data (what would come from database)
    sales_data = [
        {"date": "2024-01-01", "amount_cents": 599, "product": "Coffee", "customer_id": "CUST001"},
        {"date": "2024-01-01", "amount_cents": 850, "product": "Sandwich", "customer_id": "CUST002"},
        {"date": "2024-01-02", "amount_cents": 599, "product": "Coffee", "customer_id": "CUST001"},
        {"date": "2024-01-02", "amount_cents": 450, "product": "Pastry", "customer_id": "CUST003"},
        {"date": "2024-01-08", "amount_cents": 699, "product": "Latte", "customer_id": "CUST004"},
    ]
    
    print("Sample Data:")
    for sale in sales_data:
        print(f"  {sale['date']}: {sale['product']} - ${sale['amount_cents']/100:.2f}")
    
    # Algorithm: Single-pass aggregation
    total_cents = 0
    total_sales = 0
    
    for sale in sales_data:
        total_cents += sale['amount_cents']
        total_sales += 1
    
    avg_cents = total_cents / total_sales if total_sales > 0 else 0
    
    print(f"\nResults:")
    print(f"  Total Revenue: ${total_cents/100:.2f}")
    print(f"  Total Sales: {total_sales}")
    print(f"  Average Order Value: ${avg_cents/100:.2f}")
    
    return {"total_revenue": total_cents/100, "total_sales": total_sales, "avg_order": avg_cents/100}

def demonstrate_top_products():
    """Show top products algorithm using dictionary aggregation"""
    print("\n=== TOP PRODUCTS ALGORITHM ===")
    
    sales_data = [
        {"product": "Coffee", "amount_cents": 599},
        {"product": "Sandwich", "amount_cents": 850},
        {"product": "Coffee", "amount_cents": 599},  # Coffee appears again
        {"product": "Pastry", "amount_cents": 450},
        {"product": "Latte", "amount_cents": 699},
        {"product": "Coffee", "amount_cents": 599},  # Coffee again
    ]
    
    print("Algorithm: Dictionary for O(1) lookups")
    
    # Data Structure: Dictionary (HashMap) for fast aggregation
    product_totals = {}  # O(1) lookup time
    product_counts = {}
    
    for sale in sales_data:
        product = sale['product']
        amount = sale['amount_cents']
        
        # Update totals using dictionary
        product_totals[product] = product_totals.get(product, 0) + amount
        product_counts[product] = product_counts.get(product, 0) + 1
    
    print(f"\nProduct Aggregation:")
    for product, total_cents in product_totals.items():
        count = product_counts[product]
        print(f"  {product}: ${total_cents/100:.2f} ({count} sales)")
    
    # Algorithm: Sort by value (revenue)
    sorted_products = sorted(product_totals.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\nTop Products (sorted by revenue):")
    for i, (product, total_cents) in enumerate(sorted_products[:3], 1):
        count = product_counts[product]
        print(f"  {i}. {product}: ${total_cents/100:.2f} ({count} sales)")
    
    return sorted_products

def demonstrate_repeat_customers():
    """Show repeat customer identification using set operations"""
    print("\n=== REPEAT CUSTOMERS ALGORITHM ===")
    
    sales_data = [
        {"customer_id": "CUST001", "date": "2024-01-01"},
        {"customer_id": "CUST002", "date": "2024-01-01"},
        {"customer_id": "CUST001", "date": "2024-01-02"},  # CUST001 repeats
        {"customer_id": "CUST003", "date": "2024-01-02"},
        {"customer_id": "CUST002", "date": "2024-01-08"},  # CUST002 repeats
        {"customer_id": "CUST004", "date": "2024-01-08"},
    ]
    
    print("Algorithm: Dictionary counting + Set for unique results")
    
    # Data Structure: Dictionary for counting purchases per customer
    customer_purchases = {}
    
    for sale in sales_data:
        customer_id = sale['customer_id']
        customer_purchases[customer_id] = customer_purchases.get(customer_id, 0) + 1
    
    print(f"\nCustomer Purchase Counts:")
    for customer, count in customer_purchases.items():
        print(f"  {customer}: {count} purchases")
    
    # Algorithm: Filter customers with count > 1
    repeat_customers = {customer for customer, count in customer_purchases.items() if count > 1}
    
    print(f"\nRepeat Customers (purchased more than once):")
    for customer in repeat_customers:
        count = customer_purchases[customer]
        print(f"  {customer}: {count} purchases")
    
    print(f"\nTotal Repeat Customers: {len(repeat_customers)}")
    
    return repeat_customers

def demonstrate_csv_processing():
    """Show CSV processing algorithm with validation"""
    print("\n=== CSV PROCESSING ALGORITHM ===")
    
    # Sample CSV content as string
    csv_content = """date,product_name,amount,customer_id
2024-01-15,Coffee,5.99,CUST001
2024-01-15,Invalid Amount,abc,CUST002
2024-01-16,Sandwich,8.50,CUST003
2024-01-16,,7.99,CUST004"""
    
    print("Sample CSV Content:")
    print(csv_content)
    
    # Algorithm: Line-by-line processing with error collection
    lines = csv_content.strip().split('\n')
    headers = lines[0].split(',')
    
    print(f"\nHeaders detected: {headers}")
    
    processed_records = []
    errors = []
    
    for i, line in enumerate(lines[1:], start=2):  # Skip header, start counting from row 2
        try:
            values = line.split(',')
            record = dict(zip(headers, values))
            
            # Validation logic
            if not record['product_name'].strip():
                errors.append(f"Row {i}: Product name is empty")
                continue
                
            try:
                amount = float(record['amount'])
                if amount <= 0:
                    errors.append(f"Row {i}: Amount must be positive")
                    continue
                amount_cents = int(amount * 100)  # Convert to cents
            except ValueError:
                errors.append(f"Row {i}: Invalid amount '{record['amount']}'")
                continue
            
            # Valid record
            processed_record = {
                'date': record['date'],
                'product_name': record['product_name'],
                'amount_cents': amount_cents,
                'customer_id': record['customer_id']
            }
            processed_records.append(processed_record)
            
        except Exception as e:
            errors.append(f"Row {i}: Processing error - {str(e)}")
    
    print(f"\nProcessing Results:")
    print(f"  ✅ Successfully processed: {len(processed_records)} records")
    print(f"  ❌ Errors found: {len(errors)}")
    
    if errors:
        print(f"\nError Details:")
        for error in errors:
            print(f"  - {error}")
    
    if processed_records:
        print(f"\nValid Records:")
        for record in processed_records:
            print(f"  {record['date']}: {record['product_name']} - ${record['amount_cents']/100:.2f}")
    
    return processed_records, errors

def explain_performance_optimizations():
    """Explain the performance concepts we use"""
    print("\n=== PERFORMANCE OPTIMIZATIONS EXPLAINED ===")
    
    print("\n1. 🗂️  DATA STRUCTURES CHOICE:")
    print("   Dictionary/HashMap: O(1) average lookup time")
    print("   Example: product_totals[product] = product_totals.get(product, 0) + amount")
    print("   Why: Much faster than searching through lists O(n)")
    
    print("\n2. 💰 MONEY HANDLING:")
    print("   Store as integers (cents): 599 instead of 5.99")
    print("   Why: Avoids floating-point precision errors")
    print("   Example: 0.1 + 0.2 = 0.30000000000000004 (float)")
    print("   Example: 10 + 20 = 30 (integer cents)")
    
    print("\n3. 🔄 ALGORITHM EFFICIENCY:")
    print("   Single-pass processing: Read data once, calculate everything")
    print("   Batch processing: Handle large files in chunks")
    print("   SQL aggregation: Let database do heavy lifting")
    
    print("\n4. 📊 DATABASE INDEXING:")
    print("   Index on 'date' column → Fast time-range queries")
    print("   Index on 'customer_id' → Fast repeat customer analysis")
    print("   Why: Database can jump directly to relevant rows")

def main():
    """Run complete logic demonstration"""
    print("🎯 RETAIL ANALYTICS - BACKEND LOGIC WALKTHROUGH")
    print("=" * 60)
    
    # Demonstrate each algorithm
    revenue_metrics = demonstrate_revenue_calculation()
    top_products = demonstrate_top_products()
    repeat_customers = demonstrate_repeat_customers()
    processed_records, errors = demonstrate_csv_processing()
    explain_performance_optimizations()
    
    print("\n" + "=" * 60)
    print("✅ LOGIC WALKTHROUGH COMPLETE!")
    print("\n🎓 KEY LEARNINGS:")
    print("   • Use dictionaries for fast lookups and aggregations")
    print("   • Store money as integers to avoid precision errors")
    print("   • Collect errors instead of failing fast")
    print("   • Let databases handle heavy computations")
    print("   • Design for performance from the start")

if __name__ == "__main__":
    main()