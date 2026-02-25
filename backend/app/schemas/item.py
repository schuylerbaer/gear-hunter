from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class ItemCreate(BaseModel):
    # The 'Container' info from BeautifulSoup
    url: str
    source_id: int       # e.g., 1 for MountainProject
    category_id: int     # e.g., 1 for Shoes
    raw_text: Optional[str] = None
    author: Optional[str] = None
    
    # The 'Extracted Details' from the AI (The dictionary)
    attributes: Dict[str, str]
