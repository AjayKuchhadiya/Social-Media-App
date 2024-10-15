from jose import JWTError, jwt
from datetime import datetime, timedelta
import schema, database, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "345j43j5h4hk43hhiu5h43uhi34h54tsettht"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUTE = 30

def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTE)
    to_encode.update({'exp' : expire})

    encoded_jwt = jwt.encode(to_encode, key = SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token : str, credentials_exception): 
    try : 
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])

        id : str = payload.get('user_id')
        # print('id : ' , id)
        if id is None : 
            raise credentials_exception
        token_data = schema.TokenData(id=str(id))

    except JWTError: 
        raise credentials_exception
    
    return token_data

# We provide this funciton as a dependency to the routes that are meant to be protected and can only be accessed if the user is logged in 
def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)): 

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail= "Could not validate credentials", 
                                          headers= {"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user