from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic.config import ConfigDict

# ----------- Category schemas -----------
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class CategoryCreate(CategoryBase):
    pass

class CategoryShort(BaseModel):
    id: int
    name: str
    description: str
    model_config = ConfigDict(from_attributes=True)

class Category(CategoryBase):
    id: int
    exercises: List[ExerciseShort] = []
    model_config = ConfigDict(from_attributes=True)


# ----------- Exercise schemas -----------

class ExerciseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    video_url: Optional[str] = Field(None, max_length=300)
    image_url: Optional[str] = Field(None, max_length=300)
    duration_based: Optional[bool] = Field(False)

class ExerciseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    video_url: Optional[str] = Field(None, max_length=300)
    image_url: Optional[str] = Field(None, max_length=300)
    duration_based: Optional[bool] = None
    category_id: Optional[int] = Field(None, gt=0)

class ExerciseCreate(ExerciseBase):
    category_id: int = Field(..., gt=0)

class ExerciseShort(BaseModel):
    id: int
    name: str
    description: Optional[str]
    video_url: Optional[str]
    image_url: Optional[str]
    duration_based: Optional[bool]
    model_config = ConfigDict(from_attributes=True)

class Exercise(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None
    duration_based: Optional[bool]
    category: Optional[CategoryShort]
    workouts: List[WorkoutShort] = []

    model_config = ConfigDict(from_attributes=True)


# ----------- Workout schemas -----------

class WorkoutBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class WorkoutExerciseSchema(BaseModel):
    exercise_id: int = Field(..., gt=0)
    sets: int = Field(1, ge=1)
    reps: Optional[int] = Field(None, ge=1)
    duration: Optional[int] = Field(None, ge=1)
    rest_time_between: int = Field(0, ge=0)
    rest_time_after: int = Field(0, ge=0)

class WorkoutCreate(WorkoutBase):
    exercises: List[WorkoutExerciseSchema] = Field(default=[])

class WorkoutShort(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class WorkoutExerciseDetail(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None
    duration_based: Optional[bool] = None
    sets: int
    reps: Optional[int] = None
    duration: Optional[int] = None
    rest_time_between: int
    rest_time_after: int

    model_config = ConfigDict(from_attributes=True)

class Workout(BaseModel):
    id: int
    name: str
    exercises: List[WorkoutExerciseDetail] = []

    model_config = ConfigDict(from_attributes=True)


# ----------- Challenge schemas -----------

class ChallengeBase(BaseModel):
    name: str
    description: Optional[str] = None
    count_reps: bool
    duration: Optional[int] = None
    measurement_method: str

class ChallengeCreate(ChallengeBase):
    exercise_id: int

class Challenge(ChallengeBase):
    id: int
    exercise: ExerciseShort

    model_config = ConfigDict(from_attributes=True)







