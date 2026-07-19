from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.user import User
from app.auth.hashing import hash_password


db: Session = SessionLocal()

username = "admin"

existing = db.query(User).filter(User.username == username).first()

if existing:
    print("Admin already exists.")
    exit()

admin = User(
    username="admin",
    full_name="System Administrator",
    email="admin@railway.local",
    password_hash=hash_password("Admin@123"),
    role="Admin",
)

db.add(admin)
db.commit()

print("Admin created successfully.")