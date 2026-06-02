import os
from flask import Blueprint, send_file, abort
from services.converter_orchestrator import (
    get_job, get_job_file_path, get_job_original_name, mark_downloaded,
)

download_bp = Blueprint('download', __name__)


@download_bp.route('/api/download/<job_id>', methods=['GET'])
def download_file(job_id):
    job = get_job(job_id)
    if not job or not job['result']:
        abort(404, description='Job not found or not ready')

    original_name = get_job_original_name(job_id) or 'converted_file'
    output_path = get_job_file_path(job_id)

    if not output_path or not os.path.exists(output_path):
        abort(404, description='File not found')

    orig_base = os.path.splitext(original_name)[0]
    out_ext = os.path.splitext(output_path)[1]
    download_name = f"{orig_base}_converted{out_ext}"

    response = send_file(output_path, as_attachment=True, download_name=download_name)

    @response.call_on_close
    def cleanup():
        try:
            mark_downloaded(job_id)
        except:
            pass

    return response
