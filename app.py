import os
from flask import Flask
from flask_cors import CORS
from config import Config

os.makedirs(Config.TEMP_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.TEMP_CONVERTED_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

from routes.formats import formats_bp
from routes.conversion import conversion_bp
from routes.download import download_bp

app.register_blueprint(formats_bp)
app.register_blueprint(conversion_bp)
app.register_blueprint(download_bp)

@app.errorhandler(413)
def too_large(e):
    return {'success': False, 'error': 'File too large. Maximum 100MB'}, 413

@app.errorhandler(404)
def not_found(e):
    return {'success': False, 'error': 'Endpoint not found'}, 404

@app.errorhandler(500)
def server_error(e):
    return {'success': False, 'error': 'Internal server error'}, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
