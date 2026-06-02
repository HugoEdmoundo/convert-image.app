import os
from PIL import Image, ImageOps
from utils.file_utils import unique_output_path


def convert_image(input_path: str, output_format: str, quality: int = 92) -> dict:
    try:
        img = Image.open(input_path)
        original_format = img.format or 'Unknown'
        orig_size = img.size

        if output_format in ('jpg', 'jpeg'):
            if img.mode in ('RGBA', 'LA', 'P'):
                bg = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    bg.paste(img, mask=img.split()[-1])
                else:
                    bg.paste(img)
                img = bg
            elif img.mode != 'RGB':
                img = img.convert('RGB')
        elif output_format == 'png':
            if img.mode not in ('RGBA', 'LA'):
                if img.mode == 'P' and 'transparency' in img.info:
                    img = img.convert('RGBA')
                else:
                    img = img.convert('RGB')

        ext = f'.{output_format}'
        output_path = unique_output_path('image', ext)

        save_kwargs = {}
        if output_format in ('jpg', 'jpeg'):
            save_kwargs['quality'] = quality
            save_kwargs['optimize'] = True
            if quality >= 90:
                save_kwargs['subsampling'] = 0
        elif output_format == 'png':
            save_kwargs['optimize'] = True
            save_kwargs['compress_level'] = 6
        elif output_format == 'webp':
            save_kwargs['quality'] = quality
            save_kwargs['method'] = 6
        elif output_format == 'tiff':
            save_kwargs['compression'] = 'tiff_lzw'

        img.save(output_path, format=output_format.upper(), **save_kwargs)
        img.close()

        file_size = os.path.getsize(output_path)

        return {
            'success': True,
            'output_path': output_path,
            'original_format': original_format,
            'file_size': file_size,
            'dimensions': f"{orig_size[0]}×{orig_size[1]}",
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}
