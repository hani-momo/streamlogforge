from pydantic import BaseModel
from datetime import datetime
from typing import Optional

## python version of log_event.json
class LogEvent(BaseModel):
    timestamp: datetime
    level: str
    service: str
    message: str
    trace_id: Optional[str]
    tenant_id: str
