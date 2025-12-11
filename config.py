import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'interview_simulator.db')
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS