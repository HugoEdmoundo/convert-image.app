import os
import subprocess
import json
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


def get_video_info(input_path: str) -> dict:
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', input_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except:
        return {}


def convert_video(input_path: str, output_format: str) -> dict:
    if not check_ffmpeg():
        return {'success': False, 'error': 'FFmpeg is not installed. Install FFmpeg to enable video conversion.'}

    try:
        info = get_video_info(input_path)
        ext = f'.{output_format}'
        if output_format == 'gif':
            ext = '.gif'
        output_path = unique_output_path('video', ext)

        codec_map = {
            'mp4': 'libx264',
            'avi': 'libx264',
            'mkv': 'libx264',
            'mov': 'libx264',
            'webm': 'libvpx',
            'gif': None,
        }

        acodec_map = {
            'mp4': 'aac',
            'avi': 'mp3',
            'mkv': 'aac',
            'mov': 'aac',
            'webm': 'libvorbis',
            'gif': None,
        }

        if output_format == 'gif':
            palette = unique_output_path('palette', '.png')
            subprocess.run([
                'ffmpeg', '-i', input_path,
                '-vf', 'fps=10,scale=320:-1:flags=lanczos,palettegen=stats_mode=diff',
                '-y', palette
            ], capture_output=True, check=True)
            subprocess.run([
                'ffmpeg', '-i', input_path, '-i', palette,
                '-lavfi', 'fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse',
                '-y', output_path
            ], capture_output=True, check=True)
            os.remove(palette)
        else:
            vcodec = codec_map[output_format]
            acodec = acodec_map[output_format]
            cmd = [
                'ffmpeg', '-i', input_path,
                '-c:v', vcodec,
                '-c:a', acodec,
                '-preset', 'fast',
                '-y', output_path
            ]
            subprocess.run(cmd, capture_output=True, check=True)

        file_size = os.path.getsize(output_path)

        return {
            'success': True,
            'output_path': output_path,
            'file_size': file_size,
        }
    except subprocess.CalledProcessError as e:
        return {'success': False, 'error': f'Video conversion failed: {e.stderr.decode() if e.stderr else str(e)}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
