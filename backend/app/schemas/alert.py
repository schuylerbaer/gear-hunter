from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

# ==========================================
# CRITERIA SCHEMAS (The Key-Value pairs)
# ==========================================
class AlertCriteriaBase(BaseModel):
    key: str
    value: str

class AlertCriteria(AlertCriteriaBase):
    id: int
    alert_id: int

    class Config:
        from_attributes = True

# ==========================================
# ALERT SCHEMAS (The Main Watchlist Item)
# ==========================================
class AlertBase(BaseModel):
    category_id: int
    is_active: Optional[bool] = True

class AlertCreate(AlertBase):
    # React sends a simple dictionary: {"brand": "Scarpa", "size": "41"}
    criteria: Dict[str, str]

class Alert(AlertBase):
    id: int
    user_id: int
    created_at: datetime
    
    # When sending data BACK to React, we include the nested criteria
    criteria: List[AlertCriteria] = []

    class Config:
        from_attributes = True
