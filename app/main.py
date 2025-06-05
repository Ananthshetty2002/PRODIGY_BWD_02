# app/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from typing import List

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import engine, get_db
from app.settings import settings

# If you want to auto-create tables in dev (optional; Alembic already ran migrations):
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI + MySQL CRUD")


@app.post(
    "/users",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user. Validates:
      - name (1–50 chars)
      - email (valid format, unique)
      - age (1–150)
    """
    return crud.create_user(db=db, user_in=user_in)


@app.get(
    "/users",
    response_model=List[schemas.UserRead],
    status_code=status.HTTP_200_OK,
    summary="Get all users (with optional pagination)",
)
def read_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retrieve all users, supports skip & limit for pagination.
    """
    return crud.get_users(db=db, skip=skip, limit=limit)


@app.get(
    "/users/{user_id}",
    response_model=schemas.UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get a user by ID",
)
def read_user(user_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single user by UUID string. Raises 404 if not found.
    """
    user = crud.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found.",
        )
    return user


@app.put(
    "/users/{user_id}",
    response_model=schemas.UserRead,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
)
def update_user(
    user_id: str, user_in: schemas.UserUpdate, db: Session = Depends(get_db)
):
    """
    Partially update a user's fields (name/email/age). Raises:
      - 404 if user not found
      - 400 if new email already exists
    """
    return crud.update_user(db=db, user_id=user_id, user_in=user_in)


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """
    Delete a user by ID. Raises 404 if not found.
    Returns 204 on success (no content).
    """
    crud.delete_user(db=db, user_id=user_id)
    return None


# Optional: catch ValueError (e.g. if invalid UUID formatting is passed)
@app.exception_handler(ValueError)
def value_error_handler(request, exc: ValueError):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )
