import os
from dotenv import load_dotenv
load_dotenv()

# class Config:
#     MONGO_URI = f"mongodb://{os.getenv('DB_SERVER')}/{os.getenv('DATABASE_NAME')}"


class Config:
    DB_SERVER = os.getenv("DB_SERVER")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")
    MONGO_URI = f"mongodb://{DB_SERVER}/{DATABASE_NAME}"