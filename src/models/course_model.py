from core.configs import settings
from sqlalchemy import Column, Integer, String

class CourseModel(settings.DBBaseModel):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    description = Column(String)
    aulas = Column(Integer)
