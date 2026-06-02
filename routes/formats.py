from flask import Blueprint, jsonify, request
from services.format_registry import get_all_categories, get_suggestions

formats_bp = Blueprint('formats', __name__)


@formats_bp.route('/api/formats', methods=['GET'])
def list_formats():
    cats = get_all_categories()
    return jsonify({
        'success': True,
        'categories': [{
            'id': c['id'],
            'name': c['name'],
            'emoji': c['emoji'],
            'output_formats': c['output_formats'],
        } for c in cats],
    })


@formats_bp.route('/api/formats/suggestions', methods=['GET'])
def format_suggestions():
    ext = request.args.get('ext', '').lower()
    if not ext:
        return jsonify({'success': False, 'error': 'Missing ext parameter'}), 400
    if not ext.startswith('.'):
        ext = f'.{ext}'

    result = get_suggestions(ext)
    cat = result['category']
    return jsonify({
        'success': True,
        'category': {
            'id': cat['id'],
            'name': cat['name'],
            'emoji': cat['emoji'],
        } if cat else None,
        'suggested': result['suggested'],
        'all': result['all'],
    })
