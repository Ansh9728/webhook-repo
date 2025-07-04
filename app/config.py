import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    MONGO_URI = f"mongodb://{os.getenv('DB_SERVER')}/{os.getenv('DATABASE_NAME')}"