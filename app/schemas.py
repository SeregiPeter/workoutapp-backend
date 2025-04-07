from __future__ import annotations
from pydantic import BaseModel, Field, model_validator, HttpUrl
from typing import List, Optional
from pydantic.config import ConfigDict
from enum import Enum

# ----------- Category schemas -----------
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class CategoryCreate(CategoryBase):
    pass

class CategoryShort(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class Category(CategoryBase):
    id: int
    exercises: List[ExerciseShort] = []
    model_config = ConfigDict(from_attributes=True)


# ----------- Exercise schemas -----------

class ExerciseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    video_url: Optional[HttpUrl] = Field(None, max_length=300)
    image_url: Optional[HttpUrl] = Field(None, max_length=300)
    duration_based: bool = Field(False)

class ExerciseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    video_url: Optional[HttpUrl] = Field(None, max_length=300)
    image_url: Optional[HttpUrl] = Field(None, max_length=300)
    duration_based: Optional[bool] = None
    category_id: Optional[int] = Field(None, gt=0)

class ExerciseCreate(ExerciseBase):
    category_id: int = Field(..., gt=0)

class ExerciseShort(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    video_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None
    duration_based: bool = False
    model_config = ConfigDict(from_attributes=True)

class Exercise(ExerciseBase):
    id: int
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

    @model_validator(mode="after")
    def check_reps_or_duration(cls, values):
        if (values.reps is None and values.duration is None) or (values.reps is not None and values.duration is not None):
            raise ValueError("Either 'reps' or 'duration' must be set, but not both.")
        return values

class WorkoutCreate(WorkoutBase):
    exercises: List[WorkoutExerciseSchema] = Field(default=[])

    @model_validator(mode="after")
    def check_exercises_not_empty(cls, values):
        if not values.exercises:
            raise ValueError("Workout must contain at least one exercise.")
        return values

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

class Workout(WorkoutBase):
    id: int
    exercises: List[WorkoutExerciseDetail] = []

    model_config = ConfigDict(from_attributes=True)


# ----------- Challenge schemas -----------

class MeasurementMethodEnum(str, Enum):
    DOWN_UP = "downUpMovement"
    PROXIMITY = "proximity"
    STILLNESS = "stillness"

class ChallengeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    count_reps: bool
    duration: Optional[int] = Field(None, ge=1)
    measurement_method: MeasurementMethodEnum

class ChallengeCreate(ChallengeBase):
    exercise_id: int

    @model_validator(mode="after")
    def check_count_reps_and_duration(cls, values):
        if values.count_reps and values.duration is None:
            raise ValueError("If 'count_reps' is True, 'duration' must be set.")
        if not values.count_reps and values.duration is not None:
            raise ValueError("If 'count_reps' is False, 'duration' must not be set.")
        return values

class Challenge(ChallengeBase):
    id: int
    exercise: ExerciseShort

    model_config = ConfigDict(from_attributes=True)

    






