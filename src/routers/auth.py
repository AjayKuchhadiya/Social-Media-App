from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
import schema, models, oauth2
from database import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(tags= ['Authentication'])

@router.post('/login', response_model=schema.Token)
def login(user_credentials : schema.UserLogin, db : Session = Depends(get_db)):
    # Retrieve user from database by email
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    # Check if user exists
    if not user : 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid Credentials")
    
    plain_password = user_credentials.password
    hashed_password = user.password

    # Verify password
    verify = pwd_context.verify(plain_password, hashed_password)  
    if not verify :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= 'Invalid Credentials') 

    # create token
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})

    return {'access_token' : access_token, "token_type" : 'bearer'}