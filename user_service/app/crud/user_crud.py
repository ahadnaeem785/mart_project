from app.models.user_model import User
from sqlmodel import Session , select
from fastapi import HTTPException
from app.models.user_model import UserUpdate
from app.auth import hash_password


# Add a New User to the Database
def add_new_user(user_data: User, session: Session):
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data

# Get All Users from the Database
def get_all_users(session: Session, admin_user_id: int):
    all_users = session.exec(select(User).where(User.id != admin_user_id)).all()
    return all_users

# Get User by ID
def get_user_by_id(user_id: int, session: Session):
    user = session.exec(select(User).where(User.id == user_id)).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Delete User by ID
def delete_user_by_id(user_id: int, session: Session):
    user = session.exec(select(User).where(User.id == user_id)).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User Deleted Successfully"}

# Update User by ID
def update_user_by_id(user_id: int, to_update_user_data: UserUpdate, session: Session):
    user = session.exec(select(User).where(User.id == user_id)).one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = to_update_user_data.dict(exclude_unset=True)
    if "password" in user_data:
        user_data["password"] = hash_password(user_data["password"])
    for key, value in user_data.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

    