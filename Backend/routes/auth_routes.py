from fastapi import APIRouter, HTTPException, Depends
from Backend.models import UserCreate, LoginRequest
from Backend.services.auth import create_access_token, get_db, verify_password,get_password_hash
from Backend.models import User
from sqlalchemy.orm import Session

route = APIRouter()

@route.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    new_user = User(**user.dict(), hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@route.post("/login/")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token}
