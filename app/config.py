import os
import dotenv
from hashlib import md5


class Configuration:
    dotenv.load_dotenv()
    encryptor = md5()

    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DB_CONTAINER_NAME')}:5432/{os.getenv('POSTGRES_DB')}"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DBNAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = encryptor.digest()
