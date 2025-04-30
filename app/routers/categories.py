from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

categories_router = APIRouter(prefix="/categories", tags=["categories"])


@categories_router.get("/", response_model=list[schemas.Category])
def read_categories(db: Session = Depends(database.get_db)):
    return crud.get_all_categories(db)


@categories_router.get("/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(database.get_db)):
    return crud.get_category_by_id(db, category_id)


@categories_router.post("/", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate, db: Session = Depends(database.get_db)
):
    return crud.create_category(db, category)


@categories_router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int,
    category: schemas.CategoryBase,
    db: Session = Depends(database.get_db),
):
    return crud.update_category(db, category_id, category)


@categories_router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_category(db, category_id)
