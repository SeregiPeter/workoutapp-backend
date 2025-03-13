from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

exercises_router = APIRouter(prefix="/exercises", tags=["exercises"])

@exercises_router.get("/", response_model=list[schemas.Exercise])
def read_exercises(db: Session = Depends(database.get_db)):
    return crud.get_all_exercises(db)

@exercises_router.get("/{exercise_id}", response_model=schemas.Exercise)
def read_exercise(exercise_id: int, db: Session = Depends(database.get_db)):
    return crud.get_exercise_by_id(db, exercise_id)

@exercises_router.post("/", response_model=schemas.Exercise)
def create_exercise(exercise: schemas.ExerciseCreate, db: Session = Depends(database.get_db)):
    return crud.create_exercise(db, exercise)

@exercises_router.put("/{exercise_id}", response_model=schemas.Exercise)
def update_exercise(exercise_id: int, exercise: schemas.ExerciseBase, db: Session = Depends(database.get_db)):
    return crud.update_exercise(db, exercise_id, exercise)

@exercises_router.delete("/{exercise_id}")
def delete_exercise(exercise_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_exercise(db, exercise_id)