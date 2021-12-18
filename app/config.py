'''
import os
from os.path import join,dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path,override=True)

#database uri -> "postgresql://{my_config.database_user}:{my_config.database_password}@{my_config.database_host}/{my_config.database_name}"
database_uri = str(os.environ.get('SQLALCHEMY_DATABASE_URI',None))

#oauth2
oauth2_secretkey = os.environ.get('OAUTH2_SECRETKEY',None)
oauth2_algorithm = os.environ.get('OAUTH2_ALGORITHM',None)
token_expiration_time = os.environ.get('TOKEN_EXPIRATION_TIME',None)
'''
import os
from os.path import join,dirname
from typing import Tuple
from pydantic import BaseSettings,Field
from pydantic.env_settings import SettingsSourceCallable

dotenv_path = join(dirname(__file__),'.env')
class Settings(BaseSettings):
    sqlalchemy_database_uri:str = Field(...,env="SQLALCHEMY_DATABASE_URI")
    oauth2_secretkey:str = Field(...,env="OAUTH2_SECRETKEY")
    oauth2_algorithm:str = Field(...,env="OAUTH2_ALGORITHM")
    token_expiration_time:int = Field(...,env="TOKEN_EXPIRATION_TIME")

    class Config:
        env_file = dotenv_path
        env_file_encoding = 'utf-8'        

settings = Settings(_env_file=dotenv_path, _env_file_encoding='utf-8')
print(settings.dict())