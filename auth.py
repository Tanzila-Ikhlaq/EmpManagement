from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from models import TokenData,User
from fastapi.security import OAuth2PasswordBearer
import dotenv,os

dotenv.load_dotenv()


# Secret key for JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15 

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dummy user data
fake_data = {
    "tanzila": {
        "username": "tanzila",
        "email": "ta@gmail.com",
        "hashed_password": pwd_context.hash("tanzila"),  
        "disabled": False
    }
}

# Password verification function
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#  Get password hashed function
def get_password_hash(password):
    return pwd_context.hash(password)

# Authentication function
def authenticate_user(fake_db, username: str, password: str):
    user = fake_db.get(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

# Token creation function
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Created token for user: {to_encode['sub']} with expiry: {expire}")
    return encoded_jwt

# Get current user from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #print(f"Decoded payload: {payload}")  
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        #print(f"JWT error: {e}") 
        raise credentials_exception
    
    user_dict = fake_data.get(token_data.username)
    if user_dict is None:
        #print("User not found in fake_data.")
        raise credentials_exception
    return User(**user_dict)

#  Get current active user
def get_current_active_user(current_user: User = Depends(get_current_user)):
    if  current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

