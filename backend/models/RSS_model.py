from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

class news (Enum):
    NPR = 'npr'
    TECHNICA = 'arstechnica'
    BBC = 'bbc'
    YC = 'ycCombinator'

class feed_model(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    title: str
    description: Optional[str] = None
    link: str
    date: datetime
    source: news
    comments: Optional[str] = None
