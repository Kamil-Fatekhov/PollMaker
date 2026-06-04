import bcrypt
import jwt
from sqlalchemy import select
from config import SECRET_KEY, ALGORITHM
from database import SessionDep
from datetime import datetime
from models.user import User
from schemas.user import SUserCreate, SUser
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_access_token(user_id: int) -> str:
    payload = {"sub": str(user_id)}
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)

def register_user(session: SessionDep, data: SUserCreate) -> User | None:
    query = select(User).where(User.username == data.username)
    result = session.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        return None
    hashed = hash_password(data.password)
    user = User(username=data.username, password_hash=hashed, created_at=datetime.now())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def authenticate_user(session: SessionDep, data: SUser) -> User | None:
    query = select(User).where(User.username == data.username)
    result = session.execute(query)
    existing_user = result.scalar_one_or_none()
    if not existing_user:
        return None
    hashed = existing_user.password_hash
    correct_password = verify_password(data.password, hashed)
    if correct_password:
        return existing_user
    return None
