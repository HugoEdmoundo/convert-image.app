import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads/original'
    CONVERTED_FOLDER = 'uploads/converted'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
    
    # Image settings
    MAX_IMAGE_DIMENSION = 5000
    SUPPORTED_OUTPUT_FORMATS = ['png', 'jpg', 'webp', 'bmp']