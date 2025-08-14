from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pymongo.collection import Collection
from bson import ObjectId
from models import UserSignup, UserLogin, UserResponse, NoteCreate, NoteResponse, Token
from database import get_user_collection, get_notes_collection
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION
from fastapi.security import OAuth2PasswordRequestForm

# ---------------------------
# Security Configuration
# ---------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    
    # Use the imported JWT_EXPIRATION variable
    expire_time = expires_delta or JWT_EXPIRATION
    expire = datetime.utcnow() + expire_time
    to_encode.update({"exp": expire})

    # Use the imported JWT_SECRET and JWT_ALGORITHM variables directly
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


# ---------------------------
# Router
# ---------------------------
router = APIRouter(tags=["Authentication", "Notes"])


# ---------------------------
# Auth Routes
# ---------------------------
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user: UserSignup, users: Collection = Depends(get_user_collection)):
    """
    Register a new user with strong password policy and email uniqueness check.
    """
    # Check if email already exists
    if users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email is already registered")

    hashed_password = get_password_hash(user.password)
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "role": user.role,
        "created_at": datetime.utcnow(),
    }
    inserted = users.insert_one(new_user)
    return UserResponse(
        id=str(inserted.inserted_id),
        name=user.name,
        email=user.email,
        role=user.role,
    )


# @router.post("/login")
# def login(
#     users: Collection = Depends(get_user_collection),
#     form_data: OAuth2PasswordRequestForm = Depends() # <-- CHANGE THIS
# ):
#     """
#     Authenticates user from form data and returns JWT access token.
#     """
#     # Find the user by email, using the 'username' field from the form
#     user = users.find_one({"email": form_data.username})
    
#     # Verify the user exists and the password is correct
#     if not user or not verify_password(form_data.password, user["password"]):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     # Create the access token
#     token_data = {"sub": str(user["_id"]), "role": user["role"]}
#     access_token = create_access_token(token_data)
    
#     # The response must be a dictionary for OAuth2 to work correctly
#     return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(
    users: Collection = Depends(get_user_collection),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    # --- The logic inside your function does NOT need to change ---
    user = users.find_one({"email": form_data.username})
    
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {"sub": str(user["_id"]), "role": user["role"]}
    access_token = create_access_token(token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}
# ---------------------------
# Notes Routes
# ---------------------------
@router.post("/notes", response_model=NoteResponse)
def create_note(note: NoteCreate, notes: Collection = Depends(get_notes_collection)):
    """
    Create a new note with optional AI enhancement.
    """
    note_data = {
        "title": note.title,
        "content": note.content,
        "enhanced_content": "AI-enhanced text here" if note.ai_enhance else None,
        "created_at": datetime.utcnow(),
    }
    inserted = notes.insert_one(note_data)
    return NoteResponse(id=str(inserted.inserted_id), **note_data)


@router.get("/notes", response_model=List[NoteResponse])
def get_notes(notes: Collection = Depends(get_notes_collection)):
    """
    Retrieve all notes.
    """
    results = []
    for n in notes.find():
        results.append(NoteResponse(
            id=str(n["_id"]),
            title=n["title"],
            content=n["content"],
            enhanced_content=n.get("enhanced_content"),
            created_at=n["created_at"],
        ))
    return results
