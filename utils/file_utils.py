import os
import uuid
import time
import shutil
from datetime import datetime
from config import Config


def save_upload(file_storage) -> str:
    ext = os.path.splitext(file_storage.filename)[1].lower()
    unique_name = f"{uuid.uuid4().hex}{ext}"
    dest = os.path.join(Config.TEMP_UPLOAD_FOLDER, unique_name)
    file_storage.save(dest)
    return dest


def unique_output_path(category: str, ext: str) -> str:
    name = f"{category}_{uuid.uuid4().hex[:12]}{ext}"
    return os.path.join(Config.TEMP_CONVERTED_FOLDER, name)


def cleanup_job_files(job_data: dict):
    paths = [job_data.get('input_path'), job_data.get('output_path')]
    for p in paths:
        if p and os.path.exists(p):
            try:
                os.remove(p)
            except:
                pass


def cleanup_expired(jobs: dict):
    now = time.time()
    expired = [jid for jid, j in jobs.items()
               if now - j['created_at'] > Config.JOB_EXPIRE_SECONDS]
    for jid in expired:
        cleanup_job_files(jobs[jid])
        del jobs[jid]
