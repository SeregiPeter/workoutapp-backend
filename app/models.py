from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum as PyEnum
from .schemas import MeasurementMethodEnum


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(500), nullable=False)
    
    exercises = relationship("Exercise", back_populates="category", cascade="all, delete")


class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(String(500), nullable=False)  # Nem nullable
    video_url = Column(String(300), nullable=False)    # Nem nullable
    image_url = Column(String(300), nullable=False)    # Nem nullable
    
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)  # Kötelező kategória
    duration_based = Column(Boolean, default=False, nullable=False)

    category = relationship("Category", back_populates="exercises")
    workouts = relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete")
    challenges = relationship("Challenge", back_populates="exercise", cascade="all, delete")



class Workout(Base):
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    
    exercises = relationship("WorkoutExercise", back_populates="workout", cascade="all, delete")


class WorkoutExercise(Base):
    __tablename__ = "workout_exercise"
    
    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    
    sets = Column(Integer, nullable=False, default=1)
    reps = Column(Integer, nullable=True)      # Marad nullable, validátor kezeli
    duration = Column(Integer, nullable=True)  # Marad nullable, validátor kezeli
    
    rest_time_between = Column(Integer, nullable=False, default=0)
    rest_time_after = Column(Integer, nullable=False, default=0)

    workout = relationship("Workout", back_populates="exercises")
    exercise = relationship("Exercise", back_populates="workouts")


class Challenge(Base):
    __tablename__ = "challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(String(500), nullable=False)
    count_reps = Column(Boolean, nullable=False)
    duration = Column(Integer, nullable=True)
    measurement_method = Column(
        SQLAlchemyEnum(MeasurementMethodEnum, values_callable=lambda x: [e.value for e in x]),
        nullable=False
    )
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    
    exercise = relationship("Exercise", back_populates="challenges")



