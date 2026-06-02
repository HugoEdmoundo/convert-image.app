import os
import subprocess
from utils.file_utils import unique_output_path

FFMPEG_AVAILABLE = None


def check_ffmpeg() -> bool:
    global FFMPEG_AVAILABLE
    if FFMPEG_AVAILABLE is not None:
        return FFMPEG_AVAILABLE
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        FFMPEG_AVAILABLE = True
    except (FileNotFoundError, subprocess.CalledProcessError):
        FFMPEG_AVAILABLE = False
    return FFMPEG_AVAILABLE


def convert_audio(input_path: str, output_format: str) -> dict:
    if not check_ffmpeg():
        return {'success': False, 'error': 'FFmpeg is not installed. Install FFmpeg to enable audio conversion.'}

    try:
        ext = f'.{output_format}'
        output_path = unique_output_path('audio', ext)

        codec_map = {
            'mp3': 'libmp3lame',
            'wav': 'pcm_s16le',
            'flac': 'flac',
            'aac': 'aac',
            'ogg': 'libvorbis',
            'm4a': 'aac',
            'wma': 'wmav2',
            'opus': 'libopus',
        }

        acodec = codec_map.get(output_format, 'copy')

        cmd = ['ffmpeg', '-i', input_path, '-c:a', acodec, '-y', output_path]
        if output_format == 'm4a':
            cmd.extend(['-strict', 'experimental'])

        subprocess.run(cmd, capture_output=True, check=True)

        file_size = os.path.getsize(output_path)

        return {
            'success': True,
            'output_path': output_path,
            'file_size': file_size,
        }
    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': f'Audio conversion failed: {e.stderr.decode() if e.stderr else str(e)}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
