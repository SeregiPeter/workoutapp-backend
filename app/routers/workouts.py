from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

workouts_router = APIRouter(prefix="/workouts", tags=["workouts"])

@workouts_router.get("/", response_model=list[schemas.Workout])
def read_workouts(db: Session = Depends(database.get_db)):
    return crud.get_all_workouts(db)

@workouts_router.get("/{workout_id}", response_model=schemas.Workout)
def read_workout(workout_id: int, db: Session = Depends(database.get_db)):
    return crud.get_workout_by_id(db, workout_id)

@workouts_router.post("/", response_model=schemas.Workout)
def create_workout(workout: schemas.WorkoutCreate, db: Session = Depends(database.get_db)):
    return crud.create_workout(db, workout)

@workouts_router.put("/{workout_id}", response_model=schemas.Workout)
def update_workout(workout_id: int, workout: schemas.WorkoutCreate, db: Session = Depends(database.get_db)):
    return crud.update_workout(db, workout_id, workout)

@workouts_router.delete("/{workout_id}")
def delete_workout(workout_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_workout(db, workout_id)
