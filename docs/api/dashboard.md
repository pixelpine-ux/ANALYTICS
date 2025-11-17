# Dashboard APIs

## Base URL: `/api/v1/dashboard`

### GET /kpis
Get all KPIs for dashboard display.

**Parameters:**
- `days` (optional): Number of days to analyze (default: 30)

**Response:**
```json
{
  "revenue": 15000.50,
  "profit_margin": 25.5,
  "top_products": [...],
  "repeat_customers": 45,
  "total_customers": 120,
  "avg_order_value": 125.75,
  "calculated_at": "2024-01-15T10:30:00",
  "period_days": 30
}
```

### GET /revenue-trend
Get daily revenue trend data.

**Parameters:**
- `days` (optional): Number of days (default: 30)

**Response:**
```json
[
  {
    "date": "2024-01-15",
    "revenue": 1250.00,
    "transactions": 15
  }
]
```

### GET /customer-analytics
Get customer segmentation data.

**Response:**
```json
{
  "total_customers": 120,
  "new_customers": 25,
  "repeat_customers": 45,
  "vip_customers": 12,
  "repeat_rate": 37.5
}
```

### GET /product-performance
Get top performing products.

**Parameters:**
- `limit` (optional): Number of products (default: 10)

**Response:**
```json
[
  {
    "product_name": "Widget A",
    "total_sales": 150,
    "total_revenue": 4500.00
  }
]
```

### GET /expense-breakdown
Get expense breakdown by category.

**Parameters:**
- `days` (optional): Number of days (default: 30)

**Response:**
```json
[
  {
    "category": "Operations",
    "total_amount": 2500.00,
    "expense_count": 25
  }
]
```