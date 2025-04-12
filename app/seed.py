from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from app import models

def seed_data(db: Session):
    db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
    db.execute(text("DELETE FROM workout_exercise;"))
    db.execute(text("DELETE FROM workouts;"))
    db.execute(text("DELETE FROM exercises;"))
    db.execute(text("DELETE FROM categories;"))
    db.execute(text("DELETE FROM challenges;"))
    
    db.execute(text("ALTER TABLE workout_exercise AUTO_INCREMENT = 1;"))
    db.execute(text("ALTER TABLE workouts AUTO_INCREMENT = 1;"))
    db.execute(text("ALTER TABLE exercises AUTO_INCREMENT = 1;"))
    db.execute(text("ALTER TABLE categories AUTO_INCREMENT = 1;"))
    db.execute(text("ALTER TABLE challenges AUTO_INCREMENT = 1;"))
    
    db.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
    db.commit()

    categories = [
        models.Category(name="Strength", description="Bodyweight strength exercises."),
        models.Category(name="Core", description="Core stability and endurance exercises."),
        models.Category(name="Flexibility", description="Stretching exercises for mobility."),
    ]
    db.add_all(categories)
    db.commit()
    
    exercises = [
        models.Exercise(name="Push-ups", description="Upper body strength exercise.", video_url="https://www.youtube.com/embed/IODxDxX7oi4", image_url="https://cdn-icons-png.flaticon.com/512/2548/2548536.png", duration_based=False, category_id=categories[0].id),
        models.Exercise(name="Pull-ups", description="Back and arm strength exercise.", video_url="https://www.youtube.com/embed/eGo4IYlbE5g", image_url="https://cdn-icons-png.flaticon.com/512/5147/5147034.png", duration_based=False, category_id=categories[0].id),
        models.Exercise(name="Dips", description="Triceps and shoulder strengthening.", video_url="https://www.youtube.com/embed/0326dy_-CzM", image_url="https://cdn-icons-png.flaticon.com/512/17625/17625150.png", duration_based=False, category_id=categories[0].id),
        models.Exercise(name="Plank", description="Core stabilization exercise.", video_url="https://www.youtube.com/embed/pvIjsG5Svck", image_url="https://cdn-icons-png.flaticon.com/512/3043/3043240.png", duration_based=True, category_id=categories[1].id),
        models.Exercise(name="Sit-ups", description="Core strengthening exercise.", video_url="https://www.youtube.com/embed/jDwoBqPH0jk", image_url="https://cdn-icons-png.flaticon.com/512/2548/2548423.png", duration_based=False, category_id=categories[1].id),
        models.Exercise(name="Leg raises", description="Lower abdominal exercise.", video_url="https://www.youtube.com/embed/JB2oyawG9KI", image_url="https://cdn-icons-png.flaticon.com/512/10741/10741786.png", duration_based=False, category_id=categories[1].id),
        models.Exercise(name="Hamstring stretch", description="Stretching for the back of the legs.", video_url="https://www.youtube.com/embed/9ZXFfHtpo1g", image_url="https://cdn-icons-png.flaticon.com/512/2373/2373043.png", duration_based=True, category_id=categories[2].id),
        models.Exercise(name="Shoulder stretch", description="Improves shoulder mobility.", video_url="https://www.youtube.com/embed/F8vORlyhH2w", image_url="https://cdn-icons-png.flaticon.com/512/5783/5783241.png", duration_based=True, category_id=categories[2].id),
        models.Exercise(name="Quad stretch", description="Front thigh flexibility.", video_url="https://www.youtube.com/embed/uh2TgPmcGmY", image_url="https://cdn-icons-png.flaticon.com/512/6265/6265613.png", duration_based=True, category_id=categories[2].id),
        models.Exercise(name="Squats", description="Lower body strength exercise.", video_url="https://www.youtube.com/embed/aclHkVaku9U", image_url="https://cdn-icons-png.flaticon.com/512/2548/2548536.png", duration_based=False, category_id=categories[0].id),
    ]
    db.add_all(exercises)
    db.commit()
    
    workouts = [
        models.Workout(name="Beginner Full Body"),
        models.Workout(name="Core Strength Routine"),
        models.Workout(name="Flexibility Routine"),
    ]
    db.add_all(workouts)
    db.commit()
    
    workout_exercises = [
        models.WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[0].id, sets=2, reps=10, rest_time_between=5, rest_time_after=10),
        models.WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[1].id, sets=2, reps=10, rest_time_between=5, rest_time_after=10),
        models.WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[2].id, sets=2, reps=10, rest_time_between=5, rest_time_after=10),
        models.WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[9].id, sets=2, reps=10, rest_time_between=5, rest_time_after=10),
        models.WorkoutExercise(workout_id=workouts[1].id, exercise_id=exercises[3].id, sets=2, duration=10, rest_time_between=5, rest_time_after=10),
        models.WorkoutExercise(workout_id=workouts[1].id, exercise_id=exercises[4].id, sets=2, reps=10, rest_time_between=5, rest_time_after=10),
        models.WorkoutExercise(workout_id=workouts[1].id, exercise_id=exercises[5].id, sets=2, reps=10, rest_time_between=5, rest_time_after=10),
        models.WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[6].id, sets=2, duration=10, rest_time_between=5, rest_time_after=10),
        models.WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[7].id, sets=2, duration=10, rest_time_between=5, rest_time_after=10),
        models.WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[8].id, sets=2, duration=10, rest_time_between=5, rest_time_after=10),
    ]
    db.add_all(workout_exercises)
    db.commit()

    challenges = [
        models.Challenge(name="The Squat Challenge", description="Challenge yourself with squats.", count_reps=True, duration=60, measurement_method = "downUpMovement", exercise_id=exercises[9].id),
        models.Challenge(name="The Push-up Challenge", description="Challenge yourself with push-ups.", count_reps=True, duration=60, measurement_method = "proximity", exercise_id=exercises[0].id)
    ]
    db.add_all(challenges)
    db.commit()

    print("Database successfully populated with workout data!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

