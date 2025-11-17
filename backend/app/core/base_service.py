from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime
from .events import Event, EventType, event_bus

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)

class BaseService(Generic[ModelType]):
    """Base service class with event-driven capabilities"""
    
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    async def create(self, obj_data: Dict[str, Any], emit_event: bool = True) -> ModelType:
        """Create a new entity and emit event"""
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        
        if emit_event:
            await self._emit_created_event(db_obj)
        
        return db_obj
    
    async def update(self, obj_id: int, obj_data: Dict[str, Any], emit_event: bool = True) -> Optional[ModelType]:
        """Update an entity and emit event"""
        db_obj = self.db.query(self.model).filter(self.model.id == obj_id).first()
        if not db_obj:
            return None
        
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        
        self.db.commit()
        self.db.refresh(db_obj)
        
        if emit_event:
            await self._emit_updated_event(db_obj)
        
        return db_obj
    
    def get(self, obj_id: int) -> Optional[ModelType]:
        """Get entity by ID"""
        return self.db.query(self.model).filter(self.model.id == obj_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all entities with pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    async def delete(self, obj_id: int, emit_event: bool = True) -> bool:
        """Delete an entity and emit event"""
        db_obj = self.db.query(self.model).filter(self.model.id == obj_id).first()
        if not db_obj:
            return False
        
        if emit_event:
            await self._emit_deleted_event(db_obj)
        
        self.db.delete(db_obj)
        self.db.commit()
        return True
    
    async def _emit_created_event(self, obj: ModelType):
        """Emit created event - override in subclasses"""
        pass
    
    async def _emit_updated_event(self, obj: ModelType):
        """Emit updated event - override in subclasses"""
        pass
    
    async def _emit_deleted_event(self, obj: ModelType):
        """Emit deleted event - override in subclasses"""
        pass
    
    def _obj_to_dict(self, obj: ModelType) -> Dict[str, Any]:
        """Convert SQLAlchemy object to dict"""
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}