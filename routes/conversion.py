import json
import time
from flask import Blueprint, request, jsonify, Response, stream_with_context
from utils.validators import validate_file_size, validate_input_file, validate_output
from utils.file_utils import save_upload
from services.converter_orchestrator import (
    create_job, start_conversion, get_job,
)

conversion_bp = Blueprint('conversion', __name__)


@conversion_bp.route('/api/convert', methods=['POST'])
def handle_conversion():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400

    file = request.files['file']
    output_format = request.form.get('format', '').lower()

    if not output_format:
        return jsonify({'success': False, 'error': 'No output format specified'}), 400

    is_valid, msg = validate_file_size(file)
    if not is_valid:
        return jsonify({'success': False, 'error': msg}), 400

    is_valid, category_id = validate_input_file(file.filename)
    if not is_valid:
        return jsonify({'success': False, 'error': category_id}), 400

    is_valid, msg = validate_output(category_id, output_format)
    if not is_valid:
        return jsonify({'success': False, 'error': msg}), 400

    input_path = save_upload(file)
    job_id = create_job(input_path, file.filename, category_id, output_format)

    start_conversion(job_id)

    return jsonify({
        'success': True,
        'job_id': job_id,
    })


@conversion_bp.route('/api/convert/<job_id>/stream', methods=['GET'])
def stream_progress(job_id):
    job = get_job(job_id)
    if not job:
        return jsonify({'success': False, 'error': 'Job not found'}), 404

    def generate():
        last_percent = -1
        while True:
            current = get_job(job_id)
            if not current:
                yield f"event: error\ndata: {json.dumps({'message': 'Job expired'})}\n\n"
                break

            status = current['status']
            percent = status.get('percent', 0)

            if status['step'] == 'error':
                data = {'step': 'error', 'message': current['error'], 'percent': 0}
                yield f"event: progress\ndata: {json.dumps(data)}\n\n"
                break

            if percent != last_percent:
                last_percent = percent
                data = {
                    'step': status['step'],
                    'message': status['message'],
                    'percent': percent,
                }
                yield f"event: progress\ndata: {json.dumps(data)}\n\n"

            if status['step'] == 'done' and current['result']:
                yield f"event: complete\ndata: {json.dumps(current['result'])}\n\n"
                break

            time.sleep(0.5)

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
        },
    )
