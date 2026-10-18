from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from typing import Annotated
from database import SessionLocal
from models import Users
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from jose import jwt, JWTError
from typing import Optional
from pydantic import BaseModel,Field
import os


# ============================
#  Important Variables
# ============================
router=APIRouter()

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
OAuth2_bearer=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY =os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TIME=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# ============================
#  Response
# ============================

class CreateUser(BaseModel):
    
    username:str
    email:str
    password:str

# ============================
#  Get Database
# ============================

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency=Annotated[Session,Depends(get_db)]


# ============================
#  Register User
# ============================
@router.post('/register')
def register_user(db:db_dependency,new_user:CreateUser):
    user_model=Users(
        username=new_user.username,
        email=new_user.email,
        hashed_password=bcrypt_context.hash(new_user.password)
    )

    db.add(user_model)
    db.commit()

    return JSONResponse(status_code=201,content={'message':"User Created Successfully"})

# ============================================================
#  Login User (authenticate user,generate token,login)
# ============================================================
def authenticate_user(username,password,db):
    user=db.query(Users).filter(Users.username==username).first()
    if user is None:
        return False
    if bcrypt_context.verify(password,user.hashed_password):
        return user



def create_access_token(username:str,user_id:int,expires_delta:timedelta):
    encode={'sub':username,"id":user_id}
    expires=datetime.now(timezone.utc)+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)



@router.post('/login')
def login_user(db:db_dependency,form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    user=authenticate_user(form_data.username,form_data.password,db)

    if user==False:
        return "Failed Authentication"

    token=create_access_token(user.username,user.id,timedelta(minutes=TIME))
    return {'access_token':token,"token_type":'bearer'}




# ===================================================
#  get current login user
# ===================================================
def get_current_user(token: Annotated[str, Depends(OAuth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=404, detail='User not found')
        return {'username': username, 'id': user_id}
    except:
        raise HTTPException(status_code=404, detail='User not found')




