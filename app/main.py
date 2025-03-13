from fastapi import FastAPI
from .routers import categories, exercises, workouts, challenges
from .database import engine
from . import models
from fastapi.middleware.cors import CORSMiddleware

# Adatbázis táblák létrehozása
models.Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="Workout API",
    description="API for no-equipment workouts.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerek regisztrálása
app.include_router(categories.categories_router)
app.include_router(exercises.exercises_router)
app.include_router(workouts.workouts_router)
app.include_router(challenges.challenges_router)

@app.get("/")
def root():
    return {"message": "Üdvözöl a Workout API!"}