FORMAT_REGISTRY = [
    {
        'id': 'image',
        'name': 'Image',
        'emoji': '🖼️',
        'input_extensions': [
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp',
            '.tiff', '.tif', '.ico', '.svg', '.heic', '.heif',
        ],
        'output_formats': [
            {'format': 'png', 'name': 'PNG', 'mime': 'image/png', 'category': 'image'},
            {'format': 'jpg', 'name': 'JPEG', 'mime': 'image/jpeg', 'category': 'image'},
            {'format': 'webp', 'name': 'WebP', 'mime': 'image/webp', 'category': 'image'},
            {'format': 'gif', 'name': 'GIF', 'mime': 'image/gif', 'category': 'image'},
            {'format': 'bmp', 'name': 'BMP', 'mime': 'image/bmp', 'category': 'image'},
            {'format': 'tiff', 'name': 'TIFF', 'mime': 'image/tiff', 'category': 'image'},
            {'format': 'ico', 'name': 'ICO', 'mime': 'image/x-icon', 'category': 'image'},
        ],
    },
    {
        'id': 'video',
        'name': 'Video',
        'emoji': '🎬',
        'input_extensions': [
            '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv',
            '.webm', '.m4v', '.mpg', '.mpeg', '.3gp',
        ],
        'output_formats': [
            {'format': 'mp4', 'name': 'MP4', 'mime': 'video/mp4', 'category': 'video'},
            {'format': 'avi', 'name': 'AVI', 'mime': 'video/x-msvideo', 'category': 'video'},
            {'format': 'mkv', 'name': 'MKV', 'mime': 'video/x-matroska', 'category': 'video'},
            {'format': 'webm', 'name': 'WebM', 'mime': 'video/webm', 'category': 'video'},
            {'format': 'mov', 'name': 'MOV', 'mime': 'video/quicktime', 'category': 'video'},
            {'format': 'gif', 'name': 'GIF', 'mime': 'image/gif', 'category': 'image'},
        ],
    },
    {
        'id': 'audio',
        'name': 'Audio',
        'emoji': '🎵',
        'input_extensions': [
            '.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a',
            '.wma', '.opus', '.aiff', '.alac',
        ],
        'output_formats': [
            {'format': 'mp3', 'name': 'MP3', 'mime': 'audio/mpeg', 'category': 'audio'},
            {'format': 'wav', 'name': 'WAV', 'mime': 'audio/wav', 'category': 'audio'},
            {'format': 'flac', 'name': 'FLAC', 'mime': 'audio/flac', 'category': 'audio'},
            {'format': 'aac', 'name': 'AAC', 'mime': 'audio/aac', 'category': 'audio'},
            {'format': 'ogg', 'name': 'OGG', 'mime': 'audio/ogg', 'category': 'audio'},
            {'format': 'm4a', 'name': 'M4A', 'mime': 'audio/mp4', 'category': 'audio'},
            {'format': 'wma', 'name': 'WMA', 'mime': 'audio/x-ms-wma', 'category': 'audio'},
            {'format': 'opus', 'name': 'OPUS', 'mime': 'audio/opus', 'category': 'audio'},
        ],
    },
    {
        'id': 'document',
        'name': 'Document',
        'emoji': '📄',
        'input_extensions': [
            '.pdf', '.docx', '.doc', '.txt', '.rtf', '.odt',
            '.md', '.html', '.htm', '.epub',
        ],
        'output_formats': [
            {'format': 'pdf', 'name': 'PDF', 'mime': 'application/pdf', 'category': 'document'},
            {'format': 'docx', 'name': 'DOCX', 'mime': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'category': 'document'},
            {'format': 'txt', 'name': 'TXT', 'mime': 'text/plain', 'category': 'document'},
            {'format': 'md', 'name': 'Markdown', 'mime': 'text/markdown', 'category': 'document'},
            {'format': 'html', 'name': 'HTML', 'mime': 'text/html', 'category': 'document'},
            {'format': 'rtf', 'name': 'RTF', 'mime': 'application/rtf', 'category': 'document'},
        ],
    },
]


def get_category_for_extension(ext: str):
    ext = ext.lower()
    for cat in FORMAT_REGISTRY:
        if ext in cat['input_extensions']:
            return cat
    return None


def is_valid_output_format(category_id: str, output_format: str):
    for cat in FORMAT_REGISTRY:
        if cat['id'] == category_id:
            return any(of['format'] == output_format for of in cat['output_formats'])
    return False


def get_all_categories():
    return FORMAT_REGISTRY


def get_suggestions(ext: str):
    ext = ext.lower()
    cat = get_category_for_extension(ext)
    if not cat:
        return {'category': None, 'suggested': [], 'all': []}
    all_formats = []
    for c in FORMAT_REGISTRY:
        all_formats.extend(c['output_formats'])
    return {
        'category': cat,
        'suggested': cat['output_formats'],
        'all': all_formats,
    }
