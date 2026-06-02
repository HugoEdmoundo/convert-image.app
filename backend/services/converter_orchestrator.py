import os
import json
import time
import threading
import uuid
from config import Config
from services.image_service import convert_image
from services.video_service import convert_video
from services.audio_service import convert_audio
from services.document_service import convert_document
from utils.file_utils import cleanup_job_files

jobs: dict = {}
_lock = threading.Lock()

SERVICE_MAP = {
    'image': convert_image,
    'video': convert_video,
    'audio': convert_audio,
    'document': convert_document,
}

STEPS = [
    ('initializing', 'Initializing conversion...', 5),
    ('validating', 'Validating file...', 15),
    ('analyzing', 'Analyzing file format...', 25),
    ('extracting', 'Extracting source data...', 45),
    ('converting', 'Converting file...', 70),
    ('optimizing', 'Optimizing output...', 90),
    ('done', 'Conversion complete!', 100),
]


def create_job(input_path: str, original_name: str, category_id: str, output_format: str) -> str:
    job_id = uuid.uuid4().hex[:16]
    with _lock:
        jobs[job_id] = {
            'id': job_id,
            'input_path': input_path,
            'original_name': original_name,
            'category_id': category_id,
            'output_format': output_format,
            'output_path': None,
            'result': None,
            'status': {
                'step': 'initializing',
                'message': 'Queued...',
                'percent': 0,
            },
            'error': None,
            'created_at': time.time(),
        }
    return job_id


def start_conversion(job_id: str):
    thread = threading.Thread(target=_run_conversion, args=(job_id,), daemon=True)
    thread.start()


def _update_status(job_id: str, step: str, message: str, percent: int):
    with _lock:
        if job_id in jobs:
            jobs[job_id]['status'] = {
                'step': step,
                'message': message,
                'percent': percent,
            }


def _set_result(job_id: str, result: dict):
    with _lock:
        if job_id in jobs:
            jobs[job_id]['result'] = result


def _set_error(job_id: str, error: str):
    with _lock:
        if job_id in jobs:
            jobs[job_id]['error'] = error
            jobs[job_id]['status'] = {
                'step': 'error',
                'message': error,
                'percent': 0,
            }


def _run_conversion(job_id: str):
    with _lock:
        if job_id not in jobs:
            return
        job = jobs[job_id]

    input_path = job['input_path']
    category_id = job['category_id']
    output_format = job['output_format']

    converter = SERVICE_MAP.get(category_id)
    if not converter:
        _set_error(job_id, f'No converter available for category: {category_id}')
        return

    try:
        _update_status(job_id, 'validating', 'Validating file...', 15)
        if not os.path.exists(input_path):
            _set_error(job_id, 'Uploaded file not found')
            return

        _update_status(job_id, 'analyzing', 'Analyzing file format...', 25)
        time.sleep(0.3)

        _update_status(job_id, 'extracting', 'Extracting source data...', 45)
        time.sleep(0.3)

        fmt_name = output_format.upper()
        _update_status(job_id, 'converting', f'Converting to {fmt_name}...', 70)

        result = converter(input_path, output_format)

        if not result['success']:
            _set_error(job_id, result.get('error', 'Conversion failed'))
            return

        _update_status(job_id, 'optimizing', 'Optimizing output...', 90)
        time.sleep(0.2)

        output_path = result['output_path']
        file_size = result['file_size']
        size_str = f"{file_size / 1024:.1f} KB" if file_size < 1024 * 1024 else f"{file_size / (1024 * 1024):.1f} MB"

        with _lock:
            if job_id in jobs:
                jobs[job_id]['output_path'] = output_path

        _set_result(job_id, {
            'download_url': f'/api/download/{job_id}',
            'filename': os.path.basename(output_path),
            'size': size_str,
            'format': fmt_name,
        })

        _update_status(job_id, 'done', 'Conversion complete!', 100)

    except Exception as e:
        _set_error(job_id, str(e))


def get_job(job_id: str) -> dict | None:
    with _lock:
        job = jobs.get(job_id)
        if job:
            return {
                'status': dict(job['status']),
                'result': dict(job['result']) if job['result'] else None,
                'error': job['error'],
                'original_name': job['original_name'],
            }
        return None


def get_job_file_path(job_id: str) -> str | None:
    with _lock:
        if job_id in jobs:
            return jobs[job_id].get('output_path')
        return None


def get_job_original_name(job_id: str) -> str | None:
    with _lock:
        if job_id in jobs:
            return jobs[job_id].get('original_name')
        return None


def mark_downloaded(job_id: str):
    with _lock:
        if job_id in jobs:
            cleanup_job_files(jobs[job_id])
            del jobs[job_id]


def cleanup_all():
    with _lock:
        for jid in list(jobs.keys()):
            cleanup_job_files(jobs[jid])
            del jobs[jid]
