# Event-Driven Architecture

## Overview
The system uses an event-driven architecture to enable real-time analytics and future marketing automation.

## Core Components

### EventBus
- **Publisher/Subscriber pattern**
- **Event storage** for audit trails
- **Error handling** for failed handlers

### Event Types
```python
SALE_CREATED, SALE_UPDATED, SALE_DELETED
CUSTOMER_CREATED, CUSTOMER_UPDATED
EXPENSE_CREATED, EXPENSE_UPDATED
KPI_CALCULATED, REPORT_GENERATED
DATA_SYNC_REQUESTED, DATA_SYNC_COMPLETED
```

### BaseService
- **Generic CRUD operations**
- **Automatic event emission**
- **Extensible for all entities**

## Event Flow
1. **Data Change** → Service method called
2. **CRUD Operation** → Database updated
3. **Event Emission** → Event published to EventBus
4. **Event Handlers** → Analytics recalculation, notifications
5. **KPI Updates** → Real-time dashboard updates

## Benefits
- **Real-time Analytics**: Immediate KPI updates
- **Audit Trail**: Complete event history
- **Marketing Ready**: Event hooks for automation
- **Scalable**: Loose coupling between components