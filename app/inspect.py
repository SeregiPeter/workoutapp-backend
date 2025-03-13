from sqlalchemy import inspect
from .database import engine  # Itt add meg az adatbázis engine-t!

insp = inspect(engine)

print("Constraints for 'exercises':", insp.get_foreign_keys('exercises'))
print("Constraints for 'workout_exercise':", insp.get_foreign_keys('workout_exercise'))