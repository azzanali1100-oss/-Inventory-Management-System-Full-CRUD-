from pydantic import BaseModel
from typing import List

class WelcomeResponse(BaseModel):
    messages: List[str]