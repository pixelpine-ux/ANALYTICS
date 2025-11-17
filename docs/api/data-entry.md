# Data Entry APIs

## Base URL: `/api/v1/entry`

### POST /quick-sale
Create a sale record quickly for manual data entry.

**Request Body:**
```json
{
  "product_name": "Widget A",
  "amount": 29.99,
  "customer_id": "CUST001",
  "category": "Electronics",
  "date": "2024-01-15T10:30:00"
}
```

**Response:**
```json
{
  "success": true,
  "sale_id": 123,
  "message": "Sale recorded successfully"
}
```

### POST /quick-customer
Create a customer record quickly.

**Request Body:**
```json
{
  "id": "CUST001",
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "customer_id": "CUST001",
  "message": "Customer created successfully"
}
```

### POST /quick-expense
Record an expense quickly.

**Request Body:**
```json
{
  "description": "Office supplies",
  "amount": 45.50,
  "category": "Operations",
  "date": "2024-01-15T10:30:00"
}
```

**Response:**
```json
{
  "success": true,
  "expense_id": 456,
  "message": "Expense recorded successfully"
}
```

### GET /suggestions/products
Get product name suggestions for autocomplete.

**Parameters:**
- `query` (optional): Search term

**Response:**
```json
["Widget A", "Widget B", "Gadget X"]
```

### GET /suggestions/customers
Get customer suggestions for autocomplete.

**Parameters:**
- `query` (optional): Search term

**Response:**
```json
[
  {"id": "CUST001", "name": "John Doe"},
  {"id": "CUST002", "name": "Jane Smith"}
]
```