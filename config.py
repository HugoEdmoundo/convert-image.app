import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    TEMP_UPLOAD_FOLDER = os.path.join(BASE_DIR, 'temp_uploads')
    TEMP_CONVERTED_FOLDER = os.path.join(BASE_DIR, 'temp_converted')
    JOB_EXPIRE_SECONDS = 300
    SSE_POLL_INTERVAL = 0.5
