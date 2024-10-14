from jose import JWTError, jwt
from datetime import datetime, timedelta


SECRET_KEY = "345j43j5h4hk43hhiu5h43uhi34h54tsettht"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUTE = 30

def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTE)
    to_encode.update({'exp' : expire})

    encoded_jwt = jwt.encode(to_encode, key = SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
