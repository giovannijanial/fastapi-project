from typing import Optional
from pydantic import BaseModel as SCBaseModel

class CourseSchema(SCBaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str]
    aulas: int

    class Config:
        orm_mode = True