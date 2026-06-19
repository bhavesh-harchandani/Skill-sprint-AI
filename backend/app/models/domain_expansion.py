from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class DomainExpansion(Base):
    __tablename__ = "domain_expansions"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, nullable=False, unique=True, index=True)
    expanded_at = Column(DateTime(timezone=True), server_default=func.now())
    items_generated = Column(Integer, default=0)
    is_expanding = Column(Boolean, default=False)  # Lock to prevent concurrent expansions
    
    def __repr__(self):
        return f"<DomainExpansion {self.domain} ({self.items_generated} items)>"
