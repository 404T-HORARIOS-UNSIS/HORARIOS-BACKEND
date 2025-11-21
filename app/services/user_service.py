from datetime import timedelta
from sqlalchemy.orm import Session
from app.repositories import user_repository
from app.schemas.user_schemas import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token


def register_user(db: Session, user_in: UserCreate):
    hashed = get_password_hash(user_in.password)
    user = user_repository.create_user(db, username=user_in.username, email=user_in.email, hashed_password=hashed, role=user_in.role)
    return user


def authenticate_user(db: Session, username: str, password: str):
    user = user_repository.get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_token_for_user(user, expires_delta: timedelta | None = None):
    data = {"sub": user.username}
    return create_access_token(data=data, expires_delta=expires_delta)
