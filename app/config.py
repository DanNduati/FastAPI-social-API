import os
from os.path import join,dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path,override=True)

#database uri -> "postgresql://{my_config.database_user}:{my_config.database_password}@{my_config.database_host}/{my_config.database_name}"
database_uri = str(os.environ.get('SQLALCHEMY_DATABASE_URI',None))

#oauth2 secret key
oauth2_secretkey = os.environ.get('OAUTH2_SECRETKEY',None)