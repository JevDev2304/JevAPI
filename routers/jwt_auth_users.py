from fastapi import APIRouter, Depends,HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import jwt, JWTError

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "losgatossonlosmejoresanimalesdelmundo"
router = APIRouter()
oauth2 =OAuth2PasswordBearer(tokenUrl="login")
crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db={
    "mouredev":
    {
    "username": "mouredev",
    "fullname": "Mauricio Garcia",
    "email":  "Mauricio@gmail.com",
    "disabled": False,
    "password": "$2a$12$xxWbjsNB7v/KLubn/Y3fUeHjT2jeH3JpNSzAICKGdYdOvkwhlr4R."
    },
"jevdev":
    {
    "username": "jevdev",
    "fullname": "Juan Esteban Valdés",
    "email":  "jev@gmail.com",
    "disabled": True,
    "password": "$2a$12$SjXhWP/uCfyUK1jFlZ0W7uS2n0yETwmT4gruWPeBEUVcoyQwUkeCe"
    }
}
@router.post("/login")
async def login(form : OAuth2PasswordRequestForm = Depends()):
    user_db=users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400,detail="Invalid Username")
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid Password")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = {"sub": user.username,"exp":expire}

    return {"access_token": jwt.encode(access_token,SECRET,algorithm=ALGORITHM), "token_type": "bearer"}
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


async def auth_user(token : str = Depends(oauth2)):
    try:
        username = jwt.decode(token,SECRET,algorithms=[ALGORITHM]).get("sub")

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Username is None")

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="JWT error")
    return search_user(username)

async def current_user(user:User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Inactive user")
    return user

@router.get("/aboutMe")
async def me(user: User=Depends(current_user)):
    return user
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])