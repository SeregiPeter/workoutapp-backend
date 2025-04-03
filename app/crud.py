from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from . import models, schemas

# ----------- CATEGORY METHODS -----------

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name, description = category.description)
    db.add(db_category)
    try:
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Category name already exists.")

def get_category_by_id(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found.")
    return category

def get_all_categories(db: Session):
    return db.query(models.Category).all()

def update_category(db: Session, category_id: int, category_update: schemas.CategoryBase):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found.")

    db_category.name = category_update.name
    db_category.description = category_update.description
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found.")

    db.delete(db_category)
    db.commit()
    return {"message": "Category has been deleted."}

# ----------- EXERCISE METHODS -----------

def create_exercise(db: Session, exercise: schemas.ExerciseCreate):
    category = db.query(models.Category).filter(models.Category.id == exercise.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category not found.")

    db_exercise = models.Exercise(
        name=exercise.name,
        description=exercise.description,
        video_url=exercise.video_url,
        image_url=exercise.image_url,
        category_id=exercise.category_id,
        duration_based=exercise.duration_based
    )
    db.add(db_exercise)
    try:
        db.commit()
        db.refresh(db_exercise)
        return db_exercise
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Exercise name already exists.")

def get_exercise_by_id(db: Session, exercise_id: int):
    exercise = (
        db.query(models.Exercise)
        .join(models.Category, models.Exercise.category_id == models.Category.id)
        .filter(models.Exercise.id == exercise_id)
        .first()
    )

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found.")

    return schemas.Exercise(
        id=exercise.id,
        name=exercise.name,
        description=exercise.description,
        video_url=exercise.video_url,
        image_url=exercise.image_url,
        category=exercise.category,
        duration_based=exercise.duration_based,
        workouts=[
            schemas.WorkoutShort(id=we.workout.id, name=we.workout.name)
            for we in exercise.workouts
        ]
    )

def get_all_exercises(db: Session):
    exercises = (
        db.query(models.Exercise)
        .join(models.Category, models.Exercise.category_id == models.Category.id)
        .order_by(models.Exercise.id)
        .all()
    )

    return [
        schemas.Exercise(
            id=exercise.id,
            name=exercise.name,
            description=exercise.description,
            video_url=exercise.video_url,
            image_url=exercise.image_url,
            category=exercise.category,
            duration_based=exercise.duration_based,
            workouts=[
                schemas.WorkoutShort(id=we.workout.id, name=we.workout.name)
                for we in exercise.workouts
            ]
        )
        for exercise in exercises
    ]

def update_exercise(db: Session, exercise_id: int, exercise_update: schemas.ExerciseUpdate):
    db_exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not db_exercise:
        raise HTTPException(status_code=404, detail="Workout not found.")

    if exercise_update.name is not None:
        db_exercise.name = exercise_update.name
    if exercise_update.description is not None:
        db_exercise.description = exercise_update.description
    if exercise_update.video_url is not None:
        db_exercise.video_url = exercise_update.video_url
    if exercise_update.image_url is not None:
        db_exercise.image_url = exercise_update.image_url
    if exercise_update.duration_based is not None:
        db_exercise.duration_based = exercise_update.duration_based
    if exercise_update.category_id is not None:
        db_exercise.category_id = exercise_update.category_id
    
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

def delete_exercise(db: Session, exercise_id: int):
    db_exercise = db.query(models.Exercise).filter(models.Exercise.id == exercise_id).first()
    if not db_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found.")

    db.delete(db_exercise)
    db.commit()
    return {"message": "The exercise has been deleted."}

# ----------- WORKOUT METHODS -----------

def create_workout(db: Session, workout: schemas.WorkoutCreate):
    db_workout = models.Workout(name=workout.name)
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)

    workout_exercises = []
    for we in workout.exercises:
        exercise = db.query(models.Exercise).filter(models.Exercise.id == we.exercise_id).first()
        if not exercise:
            db.rollback()
            raise HTTPException(status_code=400, detail=f"Exercise ID {we.exercise_id} not found.")
        workout_exercise = models.WorkoutExercise(
            workout_id=db_workout.id,
            exercise_id=we.exercise_id,
            sets=we.sets,
            reps=we.reps,
            duration=we.duration,
            rest_time_between = we.rest_time_between,
            rest_time_after = we.rest_time_after
        )
        db.add(workout_exercise)
        workout_exercises.append(workout_exercise)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error during workout creation.")
    
    db.refresh(db_workout)
    return schemas.Workout(
        id=db_workout.id,
        name=db_workout.name,
        exercises=[
            schemas.WorkoutExerciseDetail(
                id=we.exercise.id,
                name=we.exercise.name,
                description=we.exercise.description,
                video_url=we.exercise.video_url,
                image_url=we.exercise.image_url,
                duration_based=we.exercise.duration_based,
                sets=we.sets,
                reps=we.reps,
                duration=we.duration,
                rest_time_between=we.rest_time_between,
                rest_time_after=we.rest_time_after
            )
            for we in workout_exercises
        ]
    )

def get_workout_by_id(db: Session, workout_id: int):
    workout = db.query(models.Workout).filter(models.Workout.id == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found.")

    return schemas.Workout(
        id=workout.id,
        name=workout.name,
        exercises=[
            schemas.WorkoutExerciseDetail(
                id=we.exercise.id,
                name=we.exercise.name,
                description=we.exercise.description,
                video_url=we.exercise.video_url,
                image_url=we.exercise.image_url,
                duration_based=we.exercise.duration_based,
                sets=we.sets,
                reps=we.reps,
                duration=we.duration,
                rest_time_between=we.rest_time_between,
                rest_time_after=we.rest_time_after
            )
            for we in workout.exercises
        ]
    )

def get_all_workouts(db: Session):
    workouts = db.query(models.Workout).all()
    
    return [
        schemas.Workout(
            id=workout.id,
            name=workout.name,
            exercises=[
                schemas.WorkoutExerciseDetail(
                id=we.exercise.id,
                name=we.exercise.name,
                description=we.exercise.description,
                video_url=we.exercise.video_url,
                image_url=we.exercise.image_url,
                duration_based=we.exercise.duration_based,
                sets=we.sets,
                reps=we.reps,
                duration=we.duration,
                rest_time_between=we.rest_time_between,
                rest_time_after=we.rest_time_after
            ) for we in workout.exercises
            ]
        )
        for workout in workouts
    ]


def update_workout(db: Session, workout_id: int, workout_update: schemas.WorkoutCreate):
    db_workout = db.query(models.Workout).filter(models.Workout.id == workout_id).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found.")

    if workout_update.name:
        db_workout.name = workout_update.name

    if workout_update.exercises is not None:
        db.query(models.WorkoutExercise).filter(models.WorkoutExercise.workout_id == workout_id).delete()

        for we in workout_update.exercises:
            exercise = db.query(models.Exercise).filter(models.Exercise.id == we.exercise_id).first()
            if not exercise:
                db.rollback()
                raise HTTPException(status_code=400, detail=f"Exercise ID {we.exercise_id} does not exist.")
            workout_exercise = models.WorkoutExercise(
                workout_id=workout_id,
                exercise_id=we.exercise_id,
                sets=we.sets,
                reps=we.reps,
                duration=we.duration,
                rest_time_between = we.rest_time_between,
                rest_time_after = we.rest_time_after
            )
            db.add(workout_exercise)

    try:
        db.commit()
        db.refresh(db_workout)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error during workout update.")

    return schemas.Workout(
        id=db_workout.id,
        name=db_workout.name,
        exercises=[
            schemas.WorkoutExerciseDetail(
                id=we.exercise.id,
                name=we.exercise.name,
                description=we.exercise.description,
                video_url=we.exercise.video_url,
                image_url=we.exercise.image_url,
                duration_based=we.exercise.duration_based,
                sets=we.sets,
                reps=we.reps,
                duration=we.duration,
                rest_time_between=we.rest_time_between,
                rest_time_after=we.rest_time_after
            )
            for we in db.query(models.WorkoutExercise)
            .filter(models.WorkoutExercise.workout_id == workout_id)
            .all()
        ]
    )

def delete_workout(db: Session, workout_id: int):
    db_workout = db.query(models.Workout).filter(models.Workout.id == workout_id).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found.")

    db.delete(db_workout)
    db.commit()
    return {"message": "Workout has been deleted."}


# ----------- CHALLENGE METHODS -----------

def create_challenge(db: Session, challenge: schemas.ChallengeCreate):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == challenge.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=400, detail="Exercise does not exist.")

    db_challenge = models.Challenge(
        name=challenge.name,
        description=challenge.description,  # New field
        count_reps=challenge.count_reps,
        duration=challenge.duration,
        measurement_method=challenge.measurement_method,
        exercise_id=challenge.exercise_id
    )
    db.add(db_challenge)
    try:
        db.commit()
        db.refresh(db_challenge)
        return db_challenge
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Name of the challenge is already used.")
    
def get_challenge_by_id(db: Session, challenge_id: int):
    challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found.")
    return challenge

def get_all_challenges(db: Session):
    return db.query(models.Challenge).all()

def update_challenge(db: Session, challenge_id: int, challenge_update: schemas.ChallengeBase):
    db_challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if not db_challenge:
        raise HTTPException(status_code=404, detail="Challenge not found.")

    db_challenge.name = challenge_update.name
    db_challenge.description = challenge_update.description
    db_challenge.count_reps = challenge_update.count_reps
    db_challenge.duration = challenge_update.duration
    db_challenge.measurement_method = challenge_update.measurement_method
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

def delete_challenge(db: Session, challenge_id: int):
    db_challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if not db_challenge:
        raise HTTPException(status_code=404, detail="Challenge not found.")

    db.delete(db_challenge)
    db.commit()
    return {"message": "Challenge has been successfully deleted."}