import os
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(env_path)

DB2_DSN = os.getenv("DB2_DSN")