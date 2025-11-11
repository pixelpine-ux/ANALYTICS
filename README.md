# Retail Analytics Dashboard

A lightweight analytics web application designed for small retail shops to track sales, customers, and business performance.

## Features

- **Data Integration**: Connect to Google Sheets or upload CSV files (sales, customers, expenses)
- **Automatic KPIs**: Revenue, Profit Margin, Top Products, Repeat Customers
- **Interactive Dashboards**: Line charts, pie charts, and data tables
- **Export & Share**: PDF reports and public dashboard links
- **Admin Panel**: Customize goals and business metrics

## Tech Stack

- **Backend**: Python (FastAPI)
- **Database**: PostgreSQL / SQLite
- **Frontend**: React + Tailwind CSS + Chart.js
- **Analytics**: Optional Superset/Metabase integration

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utility functions
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   ├── utils/          # Utility functions
│   │   └── styles/         # CSS/Tailwind styles
│   ├── public/             # Static assets
│   └── package.json        # Node dependencies
├── docs/                   # Documentation
├── scripts/                # Deployment/utility scripts
└── docker-compose.yml      # Development environment
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL (optional, SQLite for development)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd retail-analytics-dashboard
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Start development servers:
```bash
# Backend (from backend directory)
uvicorn app.main:app --reload

# Frontend (from frontend directory)
npm start
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request