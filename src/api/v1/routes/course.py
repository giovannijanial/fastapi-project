from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.course_model import CourseModel
from schemas.course_schema import CourseSchema
from core.deps import get_session

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CourseSchema)
async def create(course: CourseSchema, db: AsyncSession = Depends(get_session)):
    new_course = CourseModel(name=course.name, description=course.description, aulas=course.aulas)

    db.add(new_course)
    await db.commit()

    return new_course

@router.get("/", response_model=List[CourseSchema])
async def get_all(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel)
        result = await session.execute(query)
        courses: List[CourseModel] = result.scalars().all()
        return courses
    
@router.get("/{course_id}", response_model=CourseSchema)
async def get_by_id(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course = result.scalar_one_or_none()
        if course is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        return course
    
@router.put("/{course_id}", response_model=CourseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update(course_id: int, course: CourseSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course_db = result.scalar_one_or_none()
        if course_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        
        course_db.name = course.name
        course_db.description = course.description
        course_db.aulas = course.aulas

        await session.commit()
        return course_db
    
@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(course_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == course_id)
        result = await session.execute(query)
        course = result.scalar_one_or_none()
        if course is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        
        await session.delete(course)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)