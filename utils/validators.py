import os
from werkzeug.utils import secure_filename

class FileValidator:
    def __init__(self, allowed_extensions, max_size_mb=16):
        self.allowed_extensions = allowed_extensions
        self.max_size_bytes = max_size_mb * 1024 * 1024
    
    def allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def validate_file(self, file):
        """Validate file before processing"""
        if not file or file.filename == '':
            return False, "No file selected"
        
        if not self.allowed_file(file.filename):
            return False, "File type not allowed"
        
        # Check file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset file pointer
        
        if file_size > self.max_size_bytes:
            return False, f"File too large. Max size: {self.max_size_bytes//(1024*1024)}MB"
        
        return True, "File is valid"
    
    def get_safe_filename(self, filename):
        """Get secure filename"""
        return secure_filename(filename)