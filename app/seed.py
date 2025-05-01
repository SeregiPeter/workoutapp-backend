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
        models.Category(name="Strength", description="This category includes exercises designed to build muscle strength using your bodyweight. It focuses on major muscle groups such as the chest, arms, back, and legs. These exercises improve endurance, stability, and functional power without requiring equipment, making them ideal for home workouts."),

        models.Category(name="Core", description="Core exercises target the muscles of the abdomen, lower back, and pelvis. A strong core enhances posture, balance, and stability in everyday movements and sports. These workouts improve muscular endurance and are key to injury prevention and overall strength."),

        models.Category(name="Flexibility", description="Flexibility exercises improve the range of motion of muscles and joints. Regular stretching helps prevent injuries, reduces stiffness, and enhances overall mobility. These exercises are great for warm-ups, cool-downs, or as part of a recovery routine."),
    ]
    db.add_all(categories)
    db.commit()
    
    exercises = [
        models.Exercise(name="Push-ups", description="A fundamental bodyweight exercise that builds upper body strength, especially in the chest, shoulders, and triceps. Push-ups also engage the core and improve overall muscular endurance. They can be modified for beginners or made more challenging for advanced users. Ideal for home workouts as they require no equipment. Maintaining proper form is key to avoiding injury.", video_url="https://www.youtube.com/embed/IODxDxX7oi4", image_url="https://cdn-icons-png.flaticon.com/512/2548/2548536.png", duration_based=False, category_id=categories[0].id),

        models.Exercise(name="Pull-ups", description="A powerful upper-body exercise that strengthens the back, shoulders, and arms. Pull-ups engage multiple muscle groups and improve grip strength and posture. Regular practice enhances overall upper-body control and power. This exercise typically requires a sturdy bar for proper execution.", video_url="https://www.youtube.com/embed/eGo4IYlbE5g", image_url="https://cdn-icons-png.flaticon.com/512/5147/5147034.png", duration_based=False, category_id=categories[0].id),

        models.Exercise(name="Dips", description="Dips are an effective bodyweight exercise for targeting the triceps, chest, and shoulders. They help build upper body strength and can be performed on parallel bars or a sturdy surface. Proper control during the movement is important to prevent strain on the shoulders.", video_url="https://www.youtube.com/embed/0326dy_-CzM", image_url="https://cdn-icons-png.flaticon.com/512/17625/17625150.png", duration_based=False, category_id=categories[0].id),

        models.Exercise(name="Plank", description="The plank is a key core stabilization exercise that activates abdominal muscles, shoulders, and glutes. It's excellent for improving posture, balance, and endurance. Holding the position without sagging or arching the back is essential. Ideal for building a strong foundation.", video_url="https://www.youtube.com/embed/pvIjsG5Svck", image_url="https://cdn-icons-png.flaticon.com/512/3043/3043240.png", duration_based=True, category_id=categories[1].id),

        models.Exercise(name="Sit-ups", description="Sit-ups are a classic core exercise that strengthens the abdominal muscles. They can improve muscle tone and endurance when performed with good form. It's important to avoid pulling the neck or using momentum during the movement.", video_url="https://www.youtube.com/embed/jDwoBqPH0jk", image_url="https://cdn-icons-png.flaticon.com/512/2548/2548423.png", duration_based=False, category_id=categories[1].id),

        models.Exercise(name="Leg raises", description="Leg raises effectively target the lower abdominal muscles. Lying on your back and lifting your legs in a controlled motion improves core strength. Keeping the lower back flat on the ground helps avoid strain and enhances results.", video_url="https://www.youtube.com/embed/JB2oyawG9KI", image_url="https://cdn-icons-png.flaticon.com/512/10741/10741786.png", duration_based=False, category_id=categories[1].id),

        models.Exercise(name="Hamstring stretch", description="This stretch improves flexibility and reduces tightness in the back of the legs. It can help prevent injury and ease lower back tension. Ideal as a warm-up or cool-down routine, especially for those with sedentary lifestyles.", video_url="https://www.youtube.com/embed/9ZXFfHtpo1g", image_url="https://cdn-icons-png.flaticon.com/512/2373/2373043.png", duration_based=True, category_id=categories[2].id),

        models.Exercise(name="Shoulder stretch", description="Improves shoulder mobility and helps relieve tension from daily activities or strength training. This stretch can enhance range of motion and prevent stiffness. Great as a warm-up or recovery tool.", video_url="https://www.youtube.com/embed/F8vORlyhH2w", image_url="https://cdn-icons-png.flaticon.com/512/5783/5783241.png", duration_based=True, category_id=categories[2].id),

        models.Exercise(name="Quad stretch", description="A vital stretch for improving flexibility in the front of the thighs. Helps reduce muscle tightness and improves posture and performance during leg-focused activities. Suitable for athletes and anyone with limited mobility.", video_url="https://www.youtube.com/embed/uh2TgPmcGmY", image_url="https://cdn-icons-png.flaticon.com/512/6265/6265613.png", duration_based=True, category_id=categories[2].id),

        models.Exercise(name="Squats", description="A powerful lower body exercise targeting the thighs, hips, and glutes. Squats improve strength, mobility, and balance. Proper form is crucial: keep your chest up, back straight, and knees in line with your toes. A versatile move for all fitness levels.", video_url="https://www.youtube.com/embed/aclHkVaku9U", image_url="https://cdn-icons-png.flaticon.com/512/3043/3043271.png", duration_based=False, category_id=categories[0].id),
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
        models.WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[0].id, sets=2, reps=12, rest_time_between=20, rest_time_after=30),
        models.WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[1].id, sets=2, reps=10, rest_time_between=30, rest_time_after=30),
        models.WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[2].id, sets=3, reps=8, rest_time_between=15, rest_time_after=10),
        models.WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[9].id, sets=4, reps=20, rest_time_between=5, rest_time_after=0),
        models.WorkoutExercise(workout_id=workouts[1].id, exercise_id=exercises[3].id, sets=2, duration=20, rest_time_between=5, rest_time_after=10),
        models.WorkoutExercise(workout_id=workouts[1].id, exercise_id=exercises[4].id, sets=3, reps=12, rest_time_between=15, rest_time_after=10),
        models.WorkoutExercise(workout_id=workouts[1].id, exercise_id=exercises[5].id, sets=1, reps=20, rest_time_between=0, rest_time_after=20),
        models.WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[6].id, sets=3, duration=10, rest_time_between=5, rest_time_after=10),
        models.WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[7].id, sets=2, duration=20, rest_time_between=5, rest_time_after=5),
        models.WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[8].id, sets=4, duration=10, rest_time_between=10, rest_time_after=0),
    ]
    db.add_all(workout_exercises)
    db.commit()

    challenges = [
        models.Challenge(name="The Squat Challenge", description="Hold your phone vertically in front of you and perform slow, controlled squats. The accelerometer detects motion and counts reps. Stay balanced and maintain good form. Try to perform as many squats as you can in 60 seconds.", duration=60, measurement_method = "downUpMovement", exercise_id=exercises[9].id),

        models.Challenge(name="The Push-up Challenge", description="Place your phone flat on the floor under your head. Each time you lower yourself close to the screen, the proximity sensor detects and counts the rep. Perform as many push-ups as possible in 60 seconds.", duration=60, measurement_method = "proximity", exercise_id=exercises[0].id)
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

