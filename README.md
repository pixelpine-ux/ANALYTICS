# Retail Analytics Dashboard

> Event-driven analytics platform for small retail businesses with future marketing automation capabilities.

## 🎯 **Project Status**

- ✅ **Backend**: Complete with event-driven architecture
- ✅ **Mobile App**: iOS-first analytics dashboard complete
- 🚀 **Future**: POS integration and marketing automation ready

## 🏗️ **Architecture Overview**

**Event-Driven System** with real-time analytics and future marketing automation hooks:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Entry    │───▶│  Event System   │───▶│   Analytics     │
│ • Manual Forms  │    │ • Real-time     │    │ • Live KPIs     │
│ • CSV Upload    │    │ • Audit Trail   │    │ • Dashboards    │
│ • API Imports   │    │ • Future Hooks  │    │ • Reports       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Future Marketing│
                       │ • Automation    │
                       │ • Campaigns     │
                       │ • Segmentation  │
                       └─────────────────┘
```

## 🚀 **Quick Start**

### Backend (Ready)
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
**API Documentation**: http://localhost:8000/docs

### Mobile App (iOS)
```bash
cd mobile-app
npm install
npm start
```
**iOS Simulator**: Expo development build

## 📊 **Key Features**

### **Analytics Engine**
- Real-time KPI calculations
- Revenue trends and forecasting
- Customer segmentation analysis
- Product performance metrics

### **Data Management**
- CSV bulk import with validation
- Manual data entry forms
- Event-driven data processing
- Complete audit trail

### **Future Marketing Ready**
- Customer behavior tracking
- Automated campaign triggers
- ROI measurement framework
- Personalization data pipeline

## 📁 **Project Structure**

```
ANALYTICS/
├── backend/                 # ✅ FastAPI + Event System
│   ├── app/
│   │   ├── api/            # 25+ API endpoints
│   │   ├── core/           # Event-driven architecture
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic + events
│   │   └── main.py         # FastAPI application
│   └── tests/              # ✅ Comprehensive test suite
├── mobile-app/            # ✅ React Native + iOS Design
│   ├── src/
│   │   ├── components/     # iOS-style UI components
│   │   ├── screens/        # Dashboard, AddSale, Import
│   │   ├── services/       # API integration layer
│   │   └── styles/         # iOS design system
│   └── package.json        # Expo dependencies
├── docs/                   # ✅ Complete documentation
│   ├── architecture/       # System design docs
│   ├── api/               # Endpoint documentation
│   ├── development/       # Setup & testing guides
│   ├── frontend/          # React implementation specs
│   └── user-guides/       # End-user documentation
└── scripts/               # Deployment utilities
```

## 🔗 **API Endpoints**

### **Dashboard Analytics**
- `GET /api/v1/dashboard/kpis` - Real-time KPIs
- `GET /api/v1/dashboard/revenue-trend` - Revenue trends
- `GET /api/v1/dashboard/customer-analytics` - Customer insights
- `GET /api/v1/dashboard/product-performance` - Top products

### **Data Entry**
- `POST /api/v1/entry/quick-sale` - Manual sale entry
- `POST /api/v1/entry/quick-customer` - Customer creation
- `POST /api/v1/entry/quick-expense` - Expense logging

### **Bulk Import**
- `POST /api/v1/data/upload-sales-csv` - Sales CSV upload
- `POST /api/v1/data/upload-customers-csv` - Customer CSV upload
- `POST /api/v1/data/upload-expenses-csv` - Expense CSV upload

## 📚 **Documentation**

- **[Complete Documentation](./docs/README.md)** - Full project documentation
- **[API Reference](./docs/api/)** - Endpoint specifications
- **[Setup Guide](./docs/development/setup.md)** - Development environment
- **[Mobile App](./mobile-app/README.md)** - iOS app documentation
- **[Project Status](./docs/PROJECT_STATUS.md)** - Current progress

## 🎯 **Next Steps**

1. **Mobile App Enhancement** (Current Focus)
   - App Store deployment
   - Push notifications
   - Offline mode capabilities

2. **POS Integration** (Future - 3-6 months)
   - Offline-first POS system
   - Real-time sync with analytics
   - Enhanced customer tracking

3. **Marketing Automation** (Future - 6-12 months)
   - Campaign management
   - Customer segmentation
   - Automated marketing triggers

## 🏆 **Value Proposition**

### **Immediate (Analytics)**
- Real-time business insights
- Easy data import and entry
- Professional dashboard interface
- Automated KPI calculations

### **Future (Marketing)**
- Customer behavior analysis
- Automated campaign triggers
- ROI measurement and optimization
- Personalized customer experiences

## 📄 **License**

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

**Built with ❤️ for small retail businesses**