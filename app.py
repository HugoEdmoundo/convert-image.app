from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
from PIL import Image, ImageOps
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import io
import uuid
import shutil
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-this'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'tiff'}
app.config['TEMP_FOLDER'] = 'temp_uploads'
app.config['CONVERTED_FOLDER'] = 'temp_converted'

# Create temp directories
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)
os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def clean_temp_files():
    """Clean up temp files older than 1 hour"""
    try:
        temp_folders = [app.config['TEMP_FOLDER'], app.config['CONVERTED_FOLDER']]
        
        for folder in temp_folders:
            if os.path.exists(folder):
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        # Delete files older than 1 hour
                        if os.path.getmtime(file_path) < datetime.now().timestamp() - 3600:
                            os.remove(file_path)
                    except:
                        pass
    except:
        pass

def validate_file(file):
    """Validate file before processing"""
    if not file or file.filename == '':
        return False, "Silakan pilih file gambar terlebih dahulu"
    
    if not allowed_file(file.filename):
        allowed = ", ".join(app.config['ALLOWED_EXTENSIONS'])
        return False, f"Format file tidak didukung. Gunakan: {allowed}"
    
    # Check file size
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset file pointer
    
    max_size = app.config['MAX_CONTENT_LENGTH']
    if file_size > max_size:
        return False, f"File terlalu besar. Maksimal: {max_size//(1024*1024)}MB"
    
    return True, "File valid"

def convert_image(file_stream, original_filename, output_format='png', quality=95, 
                  resize=None, rotate=0, enhance_quality=False):
    """
    Convert image with optional enhancements
    """
    try:
        # Open image
        img = Image.open(file_stream)
        
        # Store original format
        original_format = img.format or 'Unknown'
        
        # Apply rotation if needed
        if rotate != 0:
            img = img.rotate(rotate, expand=True)
        
        # Convert image mode
        if output_format.lower() in ['jpg', 'jpeg']:
            # Remove alpha channel for JPEG
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
        elif output_format.lower() == 'png':
            # Preserve transparency for PNG
            if img.mode not in ('RGBA', 'LA'):
                if img.mode == 'P' and 'transparency' in img.info:
                    img = img.convert('RGBA')
                else:
                    img = img.convert('RGB')
        
        # Apply resize if requested
        if resize and resize != 'original':
            if resize == 'small':
                new_size = (800, 600)
            elif resize == 'medium':
                new_size = (1200, 900)
            elif resize == 'large':
                new_size = (1920, 1080)
            else:
                # Custom size
                try:
                    width, height = map(int, resize.split('x'))
                    new_size = (width, height)
                except:
                    new_size = img.size
            
            # Maintain aspect ratio
            img.thumbnail(new_size, Image.Resampling.LANCZOS)
        
        # Enhance quality if requested
        if enhance_quality:
            # Increase contrast slightly
            img = ImageOps.autocontrast(img, cutoff=2)
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%H%M%S")
        name_without_ext = os.path.splitext(original_filename)[0]
        output_filename = f"{name_without_ext[:20]}_{timestamp}_{unique_id}.{output_format}"
        output_path = os.path.join(app.config['CONVERTED_FOLDER'], output_filename)
        
        # Save with appropriate settings
        save_kwargs = {}
        if output_format.lower() in ['jpg', 'jpeg']:
            save_kwargs['quality'] = quality
            save_kwargs['optimize'] = True
            if quality >= 90:
                save_kwargs['subsampling'] = 0  # No subsampling for high quality
        elif output_format.lower() == 'png':
            save_kwargs['optimize'] = True
            save_kwargs['compress_level'] = 6
        elif output_format.lower() == 'webp':
            save_kwargs['quality'] = quality
            save_kwargs['method'] = 6  # Best quality compression
        
        img.save(output_path, format=output_format.upper(), **save_kwargs)
        img.close()
        
        # Get file size
        file_size = os.path.getsize(output_path)
        
        return {
            'success': True,
            'output_path': output_path,
            'output_filename': output_filename,
            'original_format': original_format,
            'converted_format': output_format,
            'dimensions': img.size,
            'file_size': file_size
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@app.route('/')
def index():
    """Render the main page"""
    # Clean temp files on page load
    clean_temp_files()
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def handle_conversion():
    """Handle image conversion"""
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'Tidak ada file yang dipilih'})
    
    file = request.files['image']
    output_format = request.form.get('output_format', 'png').lower()
    quality = int(request.form.get('quality', 95))
    resize = request.form.get('resize', 'original')
    rotate = int(request.form.get('rotate', 0))
    enhance = request.form.get('enhance') == 'true'
    
    # Validate file
    is_valid, message = validate_file(file)
    if not is_valid:
        return jsonify({'success': False, 'error': message})
    
    # Validate output format
    supported_formats = ['png', 'jpg', 'jpeg', 'webp', 'bmp', 'gif']
    if output_format not in supported_formats:
        return jsonify({'success': False, 'error': f'Format output tidak didukung: {output_format}'})
    
    try:
        # Convert image
        result = convert_image(
            file_stream=file.stream,
            original_filename=secure_filename(file.filename),
            output_format=output_format,
            quality=quality,
            resize=resize,
            rotate=rotate,
            enhance_quality=enhance
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'filename': result['output_filename'],
                'format': result['converted_format'].upper(),
                'dimensions': f"{result['dimensions'][0]} × {result['dimensions'][1]}",
                'size': f"{(result['file_size'] / 1024):.1f} KB",
                'download_url': f"/download/{result['output_filename']}"
            })
        else:
            return jsonify({'success': False, 'error': result['error']})
            
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error konversi: {str(e)}'})

@app.route('/download/<filename>')
def download_file(filename):
    """Download converted file"""
    try:
        file_path = os.path.join(app.config['CONVERTED_FOLDER'], filename)
        
        if os.path.exists(file_path):
            # Send file
            response = send_file(
                file_path,
                as_attachment=True,
                download_name=filename
            )
            
            # Schedule file deletion after download (async would be better in production)
            @response.call_on_close
            def delete_file():
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except:
                    pass
            
            return response
        else:
            flash('File tidak ditemukan', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'Error download: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/cleanup', methods=['POST'])
def cleanup():
    """Clean up all temp files"""
    try:
        temp_folders = [app.config['TEMP_FOLDER'], app.config['CONVERTED_FOLDER']]
        
        for folder in temp_folders:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                os.makedirs(folder, exist_ok=True)
        
        return jsonify({'success': True, 'message': 'Semua file temporary telah dibersihkan'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'success': False, 'error': 'File terlalu besar. Maksimal 16MB'}), 413

if __name__ == '__main__':
    # Clean temp files on startup
    clean_temp_files()
    app.run(debug=True, host='0.0.0.0', port=5001)