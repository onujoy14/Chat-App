"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, User
from schemas import UserBase, UserUpdate

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# CREATE USER

@app.post("/users")
def create_user(user: UserBase, db: Session = Depends(get_db)):
    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        age=user.age,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# GET ALL USERS
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# GET ONE USER
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# UPDATE USER
@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.first_name is not None:
        db_user.first_name = user.first_name

    if user.last_name is not None:
        db_user.last_name = user.last_name

    if user.age is not None:
        db_user.age = user.age

    db.commit()
    db.refresh(db_user)

    return db_user

# DELETE USER
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}
"""


from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, User
from schemas import UserBase, UserUpdate, LoginSchema, UserResponse
from auth import hash_password, verify_password, create_access_token, get_current_user

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


# CREATE USER (REGISTER)
@app.post("/users", response_model=UserResponse)
def create_user(user: UserBase, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        age=user.age,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# LOGIN USER
@app.post("/login")
def login(user: LoginSchema, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(data={"sub": db_user.email})

    return {"access_token": token, "token_type": "bearer"}


# GET CURRENT USER PROFILE (PROTECTED)
@app.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# GET ALL USERS
@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


# GET ONE USER
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# UPDATE USER
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.id == user_id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user.first_name is not None:
        db_user.first_name = user.first_name

    if user.last_name is not None:
        db_user.last_name = user.last_name

    if user.age is not None:
        db_user.age = user.age

    db.commit()
    db.refresh(db_user)

    return db_user


# DELETE USER
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}
