import os
from os.path import join,dirname
from dotenv import load_dotenv
import dotenv


dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

#database creds
database_host = os.environ.get('DB_HOST',None)
database_name = os.environ.get('DB_NAME',None)
database_user = os.environ.get('DB_USER',None)
database_password = os.environ.get('DB_PASS',None)