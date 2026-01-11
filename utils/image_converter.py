from PIL import Image
import os
import io
from datetime import datetime

class ImageConverter:
    def __init__(self, upload_folder, converted_folder):
        self.upload_folder = upload_folder
        self.converted_folder = converted_folder
        
        # Create directories if they don't exist
        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(converted_folder, exist_ok=True)
    
    def convert_image(self, input_path, output_format='png', quality=95):
        """
        Convert image to specified format
        
        Args:
            input_path: Path to input image
            output_format: Desired output format (png, jpg, webp, bmp)
            quality: Quality for lossy formats (1-100)
        
        Returns:
            dict: Result with success status and file info
        """
        try:
            # Open and validate image
            with Image.open(input_path) as img:
                # Convert RGBA for PNG support
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGBA')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Generate output filename
                original_name = os.path.basename(input_path)
                name_without_ext = os.path.splitext(original_name)[0]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"{name_without_ext}_{timestamp}.{output_format}"
                output_path = os.path.join(self.converted_folder, output_filename)
                
                # Save in desired format
                save_kwargs = {}
                
                if output_format.upper() == 'JPEG' or output_format.upper() == 'JPG':
                    if img.mode == 'RGBA':
                        # Create white background for JPEG
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    save_kwargs['quality'] = quality
                    save_kwargs['optimize'] = True
                elif output_format.upper() == 'PNG':
                    save_kwargs['optimize'] = True
                elif output_format.upper() == 'WEBP':
                    save_kwargs['quality'] = quality
                
                img.save(output_path, format=output_format.upper(), **save_kwargs)
                
                return {
                    'success': True,
                    'output_path': output_path,
                    'output_filename': output_filename,
                    'original_format': Image.MIME[img.format] if img.format in Image.MIME else 'Unknown',
                    'converted_format': output_format,
                    'dimensions': img.size,
                    'file_size': os.path.getsize(output_path)
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def convert_from_memory(self, file_stream, filename, output_format='png', quality=95):
        """
        Convert image directly from file stream without saving original
        """
        try:
            # Open image from stream
            img = Image.open(file_stream)
            
            # Process image
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGBA')
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Generate output filename
            name_without_ext = os.path.splitext(filename)[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{name_without_ext}_{timestamp}.{output_format}"
            output_path = os.path.join(self.converted_folder, output_filename)
            
            # Save converted image
            save_kwargs = {}
            if output_format.upper() in ['JPEG', 'JPG']:
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                save_kwargs['quality'] = quality
                save_kwargs['optimize'] = True
            elif output_format.upper() == 'PNG':
                save_kwargs['optimize'] = True
            
            img.save(output_path, format=output_format.upper(), **save_kwargs)
            img.close()
            
            return {
                'success': True,
                'output_path': output_path,
                'output_filename': output_filename,
                'original_format': Image.MIME[img.format] if img.format in Image.MIME else 'Unknown',
                'converted_format': output_format,
                'dimensions': img.size,
                'file_size': os.path.getsize(output_path)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_file_info(self, file_path):
        """Get information about an image file"""
        try:
            with Image.open(file_path) as img:
                return {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.width,
                    'height': img.height
                }
        except Exception as e:
            return None