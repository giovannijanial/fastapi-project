from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi import Response
from src.db.in_memory import persons
from src.models.person import Person

app = FastAPI()

@app.get("/")
async def raiz():
  return {"message": "Hello World"}


@app.get("/person")
async def get_person():
  return persons

@app.get("/person/{person_id}")
async def get_person_by_id(person_id: int):
  try:
    if person_id not in persons:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return persons[person_id]
  except KeyError:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID supplied")
    
@app.post("/person", status_code=status.HTTP_201_CREATED)
async def create_person(person: Person):
  next_id: int = len(persons) + 1
  persons[next_id] = person
  person.id = next_id
  return person

@app.put("/person/{person_id}")
async def update_person(person_id: int, person: Person):
  if person_id not in persons:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
  
@app.delete("/person/{person_id}")
async def delete_person(person_id: int):
  if person_id not in persons:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
  del persons[person_id]
  # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Person deleted successfully"})
  return Response(status_code=status.HTTP_204_NO_CONTENT)

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="info")