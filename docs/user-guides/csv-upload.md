# CSV Upload Guide

## Overview
Upload bulk data using CSV files for sales, customers, and expenses.

## Supported File Types
- **Sales Data**: Transaction records
- **Customer Data**: Customer information
- **Expense Data**: Business expenses

## CSV Format Requirements

### Sales CSV Format
**Required Columns:**
- `date` - Sale date (YYYY-MM-DD format)
- `product_name` - Product name
- `amount` - Sale amount (decimal)

**Optional Columns:**
- `customer_id` - Customer identifier
- `category` - Product category

**Example:**
```csv
date,product_name,amount,customer_id,category
2024-01-15,Widget A,29.99,CUST001,Electronics
2024-01-16,Widget B,45.50,CUST002,Electronics
```

### Customers CSV Format
**Required Columns:**
- `id` - Unique customer identifier
- `name` - Customer name

**Optional Columns:**
- `email` - Customer email

**Example:**
```csv
id,name,email
CUST001,John Doe,john@example.com
CUST002,Jane Smith,jane@example.com
```

### Expenses CSV Format
**Required Columns:**
- `date` - Expense date (YYYY-MM-DD format)
- `description` - Expense description
- `amount` - Expense amount (decimal)

**Optional Columns:**
- `category` - Expense category

**Example:**
```csv
date,description,amount,category
2024-01-15,Office supplies,45.50,Operations
2024-01-16,Marketing materials,125.00,Marketing
```

## Upload Process

### 1. Prepare Your CSV File
- Ensure all required columns are present
- Use proper date format (YYYY-MM-DD)
- Use decimal format for amounts (e.g., 29.99)
- Save file with .csv extension

### 2. Upload via API
Use the appropriate endpoint:
- Sales: `POST /api/v1/data/upload-sales-csv`
- Customers: `POST /api/v1/data/upload-customers-csv`
- Expenses: `POST /api/v1/data/upload-expenses-csv`

### 3. Review Results
The API returns:
- `success`: Whether upload succeeded
- `processed_count`: Number of records processed
- `total_rows`: Total rows in CSV
- `errors`: List of validation errors (if any)

## Error Handling
Common errors and solutions:

### Missing Required Columns
**Error:** "Missing required columns: ['amount']"
**Solution:** Add the missing column to your CSV

### Invalid Date Format
**Error:** "Row 2: Invalid date format"
**Solution:** Use YYYY-MM-DD format (e.g., 2024-01-15)

### Invalid Amount
**Error:** "Row 3: Invalid amount value"
**Solution:** Use decimal format without currency symbols (e.g., 29.99)

## Best Practices
1. **Validate data** before upload
2. **Start small** - test with a few rows first
3. **Backup data** before bulk operations
4. **Check results** after upload
5. **Use templates** - download from `/api/v1/data/upload-template/{type}`