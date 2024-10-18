from pydantic_settings import BaseSettings
import os 

class Settings(BaseSettings):
    database_hostname : str
    database_password : str
    database_username : str
    database_name : str
    database_port : int
    secret_key : str
    algorithm : str
    access_token_expire_min : int

    class Config:                     # Here, we tell the pydantic to look to get the env file details
        env_file = env_file = os.path.join(os.path.dirname(__file__), '..', '.env')


setting = Settings()