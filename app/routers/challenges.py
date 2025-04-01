from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

challenges_router = APIRouter(prefix="/challenges", tags=["challenges"])

@challenges_router.get("/", response_model=list[schemas.Challenge])
def read_challenges(db: Session = Depends(database.get_db)):
    return crud.get_all_challenges(db)

@challenges_router.get("/{challenge_id}", response_model=schemas.Challenge)
def read_challenge(challenge_id: int, db: Session = Depends(database.get_db)):
    return crud.get_challenge_by_id(db, challenge_id)

@challenges_router.post("/", response_model=schemas.Challenge)
def create_challenge(challenge: schemas.ChallengeCreate, db: Session = Depends(database.get_db)):
    return crud.create_challenge(db=db, challenge=challenge)

@challenges_router.put("/{challenge_id}", response_model=schemas.Challenge)
def update_challenge(challenge_id: int, challenge: schemas.ChallengeBase, db: Session = Depends(database.get_db)):
    return crud.update_challenge(db=db, challenge_id=challenge_id, challenge_update=challenge)

@challenges_router.delete("/{challenge_id}")
def delete_challenge(challenge_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_challenge(db=db, challenge_id=challenge_id)


