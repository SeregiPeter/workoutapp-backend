import pytest
import os
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from app.main import app
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import warnings
import uuid

warnings.simplefilter("ignore", DeprecationWarning)

# .env betöltése
load_dotenv()
READONLY_API_KEY = os.getenv("API_KEY_READONLY")
FULL_ACCESS_API_KEY = os.getenv("API_KEY_FULL_ACCESS")

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def clear_database():
    db: Session = next(get_db())
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

    yield

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



# Category tests

def test_create_category():
    response = client.post(
        "/categories/", 
        json={"name": "Test Category", "description": "Test Description"}, 
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("id") is not None
    assert data["name"] == "Test Category"
    assert data["description"] == "Test Description"

def test_create_category_without_api_key():
    response = client.post(
        "/categories/", 
        json={"name": "No Key", "description": "Fails"}
    )
    assert response.status_code == 401

def test_create_category_invalid_api_key():
    response = client.post(
        "/categories/", 
        json={"name": "Wrong Key", "description": "Fails"}, 
        headers={"api_key": "invalid_key"}
    )
    assert response.status_code == 403

def test_create_category_empty_name():
    response = client.post(
        "/categories/",
        json={"name": "", "description": "No name"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 422

def test_create_category_long_name():
    long_name = "A" * 101
    response = client.post(
        "/categories/",
        json={"name": long_name, "description": "Too long name"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 422

def test_create_category_duplicate_name():
    client.post(
        "/categories/",
        json={"name": "Unique Category", "description": "First entry"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )

    response = client.post(
        "/categories/",
        json={"name": "Unique Category", "description": "Duplicate entry"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Category name already exists."

def test_create_category_long_description():
    long_desc = "A" * 501
    response = client.post(
        "/categories/",
        json={"name": "Valid Name", "description": long_desc},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 422

def test_get_categories():
    client.post(
        "/categories/", 
        json={"name": "Another Category", "description": "Description"}, 
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    response = client.get("/categories/", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_category_by_id():
    create_response = client.post(
        "/categories/", 
        json={"name": "Test Category 5", "description": "For ID Test"}, 
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert create_response.status_code == 200
    category_id = create_response.json()["id"]

    response = client.get(f"/categories/{category_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 200
    assert response.json()["id"] == category_id

def test_get_category_invalid_id():
    response = client.get("/categories/999999", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found."

def test_update_category():
    create_response = client.post(
        "/categories/", 
        json={"name": "Test Category 6", "description": "To be updated"}, 
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert create_response.status_code == 200
    category_id = create_response.json()["id"]

    response = client.put(
        f"/categories/{category_id}", 
        json={"name": "Updated Category 6", "description": "Updated Description"}, 
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Category 6"

def test_update_category_invalid_id():
    response = client.put(
        "/categories/999999", 
        json={"name": "Invalid Update", "description": "Does not exist"}, 
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found."

def test_delete_category():
    create_response = client.post(
        "/categories/", 
        json={"name": "Test Category 7", "description": "To be deleted"}, 
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert create_response.status_code == 200
    category_id = create_response.json()["id"]

    response = client.delete(f"/categories/{category_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 200
    assert response.json()["message"] == "Category has been deleted."

def test_delete_category_invalid_id():
    response = client.delete("/categories/999999", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found."

# Exercise tests

def test_create_exercise():
    category_response = client.post(
        "/categories/",
        json={"name": "Strength", "description": "Strength training exercises"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    category_id = category_response.json()["id"]

    response = client.post(
        "/exercises/",
        json={
            "name": "Push-Up",
            "description": "Upper body exercise",
            "video_url": "http://example.com/pushup.mp4",
            "image_url": "http://example.com/pushup.jpg",
            "duration_based": False,
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 200

def test_create_exercise_without_category():
    response = client.post(
        "/exercises/",
        json={
            "name": "Jumping Jack",
            "description": "Full-body warm-up",
            "category_id": 999999
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 400

def test_create_exercise_empty_name():
    response = client.post(
        "/exercises/",
        json={
            "name": "",
            "description": "Invalid",
            "category_id": 1
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 422

def test_create_exercise_long_name():
    long_name = "A" * 101
    response = client.post(
        "/exercises/",
        json={
            "name": long_name,
            "description": "Too long",
            "category_id": 1
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 422

def test_get_exercise_by_id():
    response = client.get("/exercises/1", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 200

def test_get_exercise_invalid_id():
    response = client.get("/exercises/999999", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 404

def test_get_all_exercises():
    response = client.get("/exercises/", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_exercise():
    response = client.put(
        "/exercises/1",
        json={
            "name": "Updated Exercise",
            "description": "Updated description",
            "video_url": "http://example.com/updated.mp4",
            "image_url": "http://example.com/updated.jpg",
            "duration_based": True
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 200

def test_update_exercise_invalid_id():
    response = client.put(
        "/exercises/999999",
        json={
            "name": "Invalid Update",
            "description": "Should fail"
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 404

def test_delete_exercise():
    response = client.delete("/exercises/1", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 200

def test_delete_exercise_invalid_id():
    response = client.delete("/exercises/999999", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 404


# Category - Exercise relationship tests

import uuid

def test_create_category():
    category_name = f"Cardio-{uuid.uuid4()}"
    response = client.post(
        "/categories/",
        json={"name": category_name, "description": "Cardio exercises"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 200
    assert response.json()["name"] == category_name


def test_create_exercise_with_category():
    category_name = f"Category-{uuid.uuid4()}"
    category_response = client.post(
        "/categories/",
        json={"name": category_name, "description": "Test category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]

    exercise_name = f"Jump Rope-{uuid.uuid4()}"
    response = client.post(
        "/exercises/",
        json={
            "name": exercise_name,
            "description": "Cardio exercise with a jump rope",
            "video_url": "https://example.com/jumprope.mp4",
            "image_url": "https://example.com/jumprope.jpg",
            "duration_based": True,
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 200
    assert response.json()["category"]["id"] == category_id


def test_get_category_with_exercises():
    category_name = f"Category-{uuid.uuid4()}"
    category_response = client.post(
        "/categories/",
        json={"name": category_name, "description": "Test category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]

    exercise_name = f"Jump Rope-{uuid.uuid4()}"
    client.post(
        "/exercises/",
        json={
            "name": exercise_name,
            "description": "Cardio exercise with a jump rope",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )

    response = client.get(f"/categories/{category_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 200
    assert isinstance(response.json()["exercises"], list)
    assert any(ex["name"] == exercise_name for ex in response.json()["exercises"])


def test_create_exercise_invalid_category():
    response = client.post(
        "/exercises/",
        json={
            "name": "Invalid Exercise",
            "description": "This should not be created",
            "category_id": 999999
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Category not found."


def test_delete_category_and_check_exercise():
    category_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "To be deleted"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]

    exercise_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "Exercise to be orphaned",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert exercise_response.status_code == 200
    exercise_id = exercise_response.json()["id"]

    response = client.delete(f"/categories/{category_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 200

    response = client.get(f"/exercises/{exercise_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 404


def test_update_exercise_category():
    category1_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "Old category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert category1_response.status_code == 200
    category1_id = category1_response.json()["id"]

    category2_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "New category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert category2_response.status_code == 200
    category2_id = category2_response.json()["id"]

    exercise_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "Test exercise",
            "category_id": category1_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert exercise_response.status_code == 200
    exercise_id = exercise_response.json()["id"]

    response = client.put(
        f"/exercises/{exercise_id}",
        json={
            "name": "Updated Exercise",
            "description": "Updated description",
            "category_id": category2_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 200
    assert response.json()["category"]["id"] == category2_id


def test_create_exercise_without_category():
    response = client.post(
        "/exercises/",
        json={
            "name": "Plank",
            "description": "Core strengthening exercise"
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 422


# Workout tests

def test_create_workout_without_exercises():
    workout_name = f"Workout-{uuid.uuid4()}"
    response = client.post(
        "/workouts/",
        json={"name": workout_name, "exercises": []},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert response.status_code == 422

def test_get_workout_by_id():
    category_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "Test category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]
    
    exercise1_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "First test exercise",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )

    exercise1_id = exercise1_response.json()["id"]


    workout_name = f"Workout-{uuid.uuid4()}"
    create_response = client.post(
        "/workouts/",
        json={
            "name": workout_name,
            "exercises": [
                {"exercise_id": exercise1_id, "sets": 3, "reps": 10, "rest_time_between": 30}
            ]
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert create_response.status_code == 200
    workout_id = create_response.json()["id"]

    get_response = client.get(f"/workouts/{workout_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert get_response.status_code == 200
    assert get_response.json()["id"] == workout_id
    assert get_response.json()["name"] == workout_name


def test_update_workout():
    category_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "Test category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]
    
    exercise1_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "First test exercise",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )

    exercise1_id = exercise1_response.json()["id"]


    workout_name = f"Workout-{uuid.uuid4()}"
    create_response = client.post(
        "/workouts/",
        json={
            "name": workout_name,
            "exercises": [
                {"exercise_id": exercise1_id, "sets": 3, "reps": 10, "rest_time_between": 30}
            ]
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert create_response.status_code == 200
    workout_id = create_response.json()["id"]

    updated_name = f"Updated-{uuid.uuid4()}"
    update_response = client.put(
        f"/workouts/{workout_id}",
        json={"name": updated_name, "exercises": [
                {"exercise_id": exercise1_id, "sets": 3, "reps": 10, "rest_time_between": 30}
            ]},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert update_response.status_code == 200
    assert update_response.json()["id"] == workout_id
    assert update_response.json()["name"] == updated_name


def test_delete_workout():
    category_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "Test category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]
    
    exercise1_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "First test exercise",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )

    exercise1_id = exercise1_response.json()["id"]


    workout_name = f"Workout-{uuid.uuid4()}"
    create_response = client.post(
        "/workouts/",
        json={
            "name": workout_name,
            "exercises": [
                {"exercise_id": exercise1_id, "sets": 3, "reps": 10, "rest_time_between": 30}
            ]
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert create_response.status_code == 200
    workout_id = create_response.json()["id"]

    delete_response = client.delete(f"/workouts/{workout_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert delete_response.status_code == 200

    get_response = client.get(f"/workouts/{workout_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert get_response.status_code == 404


# Workout - Exercise relationship tests

def test_create_workout_with_exercises():
    category_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "Test category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]

    exercise1_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "First test exercise",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert exercise1_response.status_code == 200
    exercise1_id = exercise1_response.json()["id"]

    exercise2_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "Second test exercise",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert exercise2_response.status_code == 200
    exercise2_id = exercise2_response.json()["id"]

    workout_response = client.post(
        "/workouts/",
        json={
            "name": f"Workout-{uuid.uuid4()}",
            "exercises": [
                {"exercise_id": exercise1_id, "sets": 3, "reps": 10, "rest_time_between": 30},
                {"exercise_id": exercise2_id, "sets": 2, "duration": 60, "rest_time_after": 60}
            ]
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert workout_response.status_code == 200
    workout_id = workout_response.json()["id"]

    get_workout_response = client.get(f"/workouts/{workout_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert get_workout_response.status_code == 200
    workout_data = get_workout_response.json()
    assert len(workout_data["exercises"]) == 2
    assert workout_data["exercises"][0]["id"] in [exercise1_id, exercise2_id]
    assert workout_data["exercises"][1]["id"] in [exercise1_id, exercise2_id]


def test_delete_exercise_and_check_workout():
    category_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "Test category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]

    exercise_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "Exercise to be deleted",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert exercise_response.status_code == 200
    exercise_id = exercise_response.json()["id"]

    workout_response = client.post(
        "/workouts/",
        json={
            "name": f"Workout-{uuid.uuid4()}",
            "exercises": [{"exercise_id": exercise_id, "sets": 3, "reps": 12}]
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert workout_response.status_code == 200
    workout_id = workout_response.json()["id"]

    delete_response = client.delete(f"/exercises/{exercise_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert delete_response.status_code == 200

    get_exercise_response = client.get(f"/exercises/{exercise_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert get_exercise_response.status_code == 404

    get_workout_response = client.get(f"/workouts/{workout_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert get_workout_response.status_code == 200
    workout_data = get_workout_response.json()
    assert len(workout_data["exercises"]) == 0

def test_delete_workout_and_check_exercises():
    category_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "Test category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]

    exercise_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "Exercise remains after workout deletion",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert exercise_response.status_code == 200
    exercise_id = exercise_response.json()["id"]

    workout_response = client.post(
        "/workouts/",
        json={
            "name": f"Workout-{uuid.uuid4()}",
            "exercises": [{"exercise_id": exercise_id, "sets": 3, "reps": 15}]
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert workout_response.status_code == 200
    workout_id = workout_response.json()["id"]

    delete_response = client.delete(f"/workouts/{workout_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert delete_response.status_code == 200

    get_workout_response = client.get(f"/workouts/{workout_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert get_workout_response.status_code == 404

    get_exercise_response = client.get(f"/exercises/{exercise_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert get_exercise_response.status_code == 200



def test_create_challenge():
    category_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "Test category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert category_response.status_code == 200
    category_id = category_response.json()["id"]

    exercise_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "Test exercise",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert exercise_response.status_code == 200
    exercise_id = exercise_response.json()["id"]

    challenge_response = client.post(
        "/challenges/",
        json={
            "name": f"Challenge-{uuid.uuid4()}",
            "description": "Test challenge",
            "count_reps": True,
            "duration": 60,
            "measurement_method": "downUpMovement",
            "exercise_id": exercise_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert challenge_response.status_code == 200
    challenge_data = challenge_response.json()
    assert challenge_data["name"].startswith("Challenge-")
    assert challenge_data["count_reps"] is True
    assert challenge_data["duration"] == 60
    assert challenge_data["measurement_method"] == "downUpMovement"
    assert challenge_data["exercise"]["id"] == exercise_id


def test_get_challenge():
    category_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "Test category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    category_id = category_response.json()["id"]

    exercise_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "Test exercise",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    exercise_id = exercise_response.json()["id"]

    challenge_response = client.post(
        "/challenges/",
        json={
            "name": f"Challenge-{uuid.uuid4()}",
            "description": "Test challenge",
            "count_reps": True,
            "duration": 60,
            "measurement_method": "downUpMovement",
            "exercise_id": exercise_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    challenge_id = challenge_response.json()["id"]

    response = client.get(f"/challenges/{challenge_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 200
    challenge_data = response.json()
    assert challenge_data["id"] == challenge_id


def test_update_challenge():
    category_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "Test category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    category_id = category_response.json()["id"]

    exercise_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "Test exercise",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    exercise_id = exercise_response.json()["id"]

    challenge_response = client.post(
        "/challenges/",
        json={
            "name": f"Challenge-{uuid.uuid4()}",
            "description": "Test challenge",
            "count_reps": True,
            "duration": 60,
            "measurement_method": "downUpMovement",
            "exercise_id": exercise_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    challenge_id = challenge_response.json()["id"]

    update_response = client.put(
        f"/challenges/{challenge_id}",
        json={
            "name": "Updated Challenge",
            "description": "Updated description",
            "count_reps": False,
            "measurement_method": "proximity"
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert update_response.status_code == 200
    updated_challenge = update_response.json()
    assert updated_challenge["name"] == "Updated Challenge"
    assert updated_challenge["description"] == "Updated description"
    assert updated_challenge["count_reps"] is False
    assert updated_challenge["duration"] is None
    assert updated_challenge["measurement_method"] == "proximity"


def test_delete_challenge():
    category_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "Test category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    category_id = category_response.json()["id"]

    exercise_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "Test exercise",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    exercise_id = exercise_response.json()["id"]

    challenge_response = client.post(
        "/challenges/",
        json={
            "name": f"Challenge-{uuid.uuid4()}",
            "description": "Test challenge",
            "count_reps": True,
            "duration": 60,
            "measurement_method": "proximity",
            "exercise_id": exercise_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    challenge_id = challenge_response.json()["id"]

    delete_response = client.delete(f"/challenges/{challenge_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Challenge has been successfully deleted."}

    get_response = client.get(f"/challenges/{challenge_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert get_response.status_code == 404



def test_create_challenge_with_invalid_exercise():
    challenge_response = client.post(
        "/challenges/",
        json={
            "name": f"Challenge-{uuid.uuid4()}",
            "description": "Test challenge",
            "count_reps": True,
            "duration": 60,
            "measurement_method": "proximity",
            "exercise_id": 999999
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    assert challenge_response.status_code == 400
    assert challenge_response.json()["detail"] == "Exercise does not exist."


def test_get_challenges_by_exercise():
    category_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "Test category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    category_id = category_response.json()["id"]

    exercise_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "Test exercise",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    exercise_id = exercise_response.json()["id"]

    for _ in range(2):
        client.post(
            "/challenges/",
            json={
                "name": f"Challenge-{uuid.uuid4()}",
                "description": "Test challenge",
                "count_reps": True,
                "duration": 60,
                "measurement_method": "proximity",
                "exercise_id": exercise_id
            },
            headers={"api_key": FULL_ACCESS_API_KEY}
        )

    challenges_response = client.get("/challenges/", headers={"api_key": FULL_ACCESS_API_KEY})
    assert challenges_response.status_code == 200
    challenges = challenges_response.json()

    exercise_challenges = [ch for ch in challenges if ch["exercise"]["id"] == exercise_id]
    assert len(exercise_challenges) >= 2


def test_delete_exercise_deletes_challenges():
    category_response = client.post(
        "/categories/",
        json={"name": f"Category-{uuid.uuid4()}", "description": "Test category"},
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    category_id = category_response.json()["id"]

    exercise_response = client.post(
        "/exercises/",
        json={
            "name": f"Exercise-{uuid.uuid4()}",
            "description": "Test exercise",
            "category_id": category_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    exercise_id = exercise_response.json()["id"]

    challenge_response = client.post(
        "/challenges/",
        json={
            "name": f"Challenge-{uuid.uuid4()}",
            "description": "Test challenge",
            "count_reps": True,
            "duration": 60,
            "measurement_method": "proximity",
            "exercise_id": exercise_id
        },
        headers={"api_key": FULL_ACCESS_API_KEY}
    )
    challenge_id = challenge_response.json()["id"]

    delete_exercise_response = client.delete(f"/exercises/{exercise_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert delete_exercise_response.status_code == 200

    get_challenge_response = client.get(f"/challenges/{challenge_id}", headers={"api_key": FULL_ACCESS_API_KEY})
    assert get_challenge_response.status_code == 404



# Api key tests

def test_access_docs_without_api_key():
    response = client.get("/docs")
    assert response.status_code == 200

def test_access_with_no_api_key():
    response = client.get("/categories/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Missing API key. Please provide an 'api_key' header!"}

def test_read_access_with_readonly_api_key():
    response = client.get("/categories/", headers={"api_key": READONLY_API_KEY})
    assert response.status_code == 200

def test_read_access_with_full_access_api_key():
    response = client.get("/categories/", headers={"api_key": FULL_ACCESS_API_KEY})
    assert response.status_code == 200

def test_write_access_with_readonly_api_key():
    response = client.post(
        "/categories/",
        json={"name": "Test Category", "description": "Test Description"},
        headers={"api_key": READONLY_API_KEY},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid API key or insufficient permissions!"}

def test_write_access_with_full_access_api_key():
    response = client.post(
        "/categories/",
        json={"name": "Test Category", "description": "Test Description"},
        headers={"api_key": FULL_ACCESS_API_KEY},
    )
    assert response.status_code == 200

def test_invalid_api_key():
    response = client.get("/categories/", headers={"api_key": "invalid-key"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid API key or insufficient permissions!"}