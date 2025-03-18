from fastapi import FastAPI, Depends
from .dependencies import get_api_key
from .routers import categories, exercises, workouts, challenges
from .database import engine
from . import models
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(categories.categories_router, dependencies=[Depends(get_api_key)])
app.include_router(exercises.exercises_router, dependencies=[Depends(get_api_key)])
app.include_router(workouts.workouts_router, dependencies=[Depends(get_api_key)])
app.include_router(challenges.challenges_router, dependencies=[Depends(get_api_key)])

@app.get("/", dependencies=[Depends(get_api_key)])
def root():
    return {"message": "Welcome to the Workout API!"}