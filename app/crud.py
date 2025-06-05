# app/crud.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional

from fastapi import HTTPException, status

from app import models, schemas


def get_user(db: Session, user_id: str) -> Optional[models.User]:
    """
    Return the User object by ID or None if not found.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    Return a User object by email, or None if not found.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """
    Return a list of users with pagination.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    """
    Create a new user.
    Raises 400 if email already exists.
    """
    # Check for duplicate email
    existing = get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{user_in.email}' is already registered.",
        )

    # Build new User ORM object
    new_user = models.User(
        name=user_in.name,
        email=user_in.email,
        age=user_in.age,
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to create user (possible duplicate email).",
        )


def update_user(db: Session, user_id: str, user_in: schemas.UserUpdate) -> models.User:
    """
    Partially update an existing user.
    Raises 404 if not found, 400 if email conflict.
    """
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )

    # If email is changing, ensure uniqueness
    if user_in.email and user_in.email != db_user.email:
        existing = get_user_by_email(db, user_in.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{user_in.email}' is already registered.",
            )

    # Update only provided fields
    if user_in.name is not None:
        db_user.name = user_in.name
    if user_in.email is not None:
        db_user.email = user_in.email
    if user_in.age is not None:
        db_user.age = user_in.age

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to update user (possible duplicate email).",
        )


def delete_user(db: Session, user_id: str) -> None:
    """
    Delete a user by ID.
    Raises 404 if user not found.
    """
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found; cannot delete.",
        )
    db.delete(db_user)
    db.commit()
    return None
