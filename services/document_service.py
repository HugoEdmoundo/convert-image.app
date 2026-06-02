import os
from utils.file_utils import unique_output_path


def convert_document(input_path: str, output_format: str) -> dict:
    ext = os.path.splitext(input_path)[1].lower()

    try:
        if output_format == 'txt':
            return _to_text(input_path, ext)
        elif output_format == 'html':
            return _to_html(input_path, ext)
        elif output_format == 'md':
            return _to_markdown(input_path, ext)
        elif output_format == 'pdf':
            return _to_pdf(input_path, ext)
        elif output_format == 'docx':
            return _to_docx(input_path, ext)
        else:
            return {'success': False, 'error': f'Document format not supported: {output_format}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def _read_text(input_path: str) -> str:
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(input_path, 'r', encoding='latin-1') as f:
            return f.read()


def _to_text(input_path: str, ext: str) -> dict:
    if ext == '.txt':
        content = _read_text(input_path)
    elif ext in ('.md', '.html', '.htm'):
        content = _read_text(input_path)
    elif ext == '.rtf':
        try:
            from striprtf.striprtf import rtf_to_text
            with open(input_path, 'r', encoding='utf-8') as f:
                content = rtf_to_text(f.read())
        except ImportError:
            content = _read_text(input_path)
    else:
        content = _read_text(input_path)

    output_path = unique_output_path('document', '.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return {'success': True, 'output_path': output_path, 'file_size': os.path.getsize(output_path)}


def _to_html(input_path: str, ext: str) -> dict:
    content = _read_text(input_path)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>Converted</title></head><body><pre>{content}</pre></body></html>"""
    if ext == '.md':
        try:
            import markdown
            html = markdown.markdown(content)
            html = f"<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>{html}</body></html>"
        except ImportError:
            pass

    output_path = unique_output_path('document', '.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return {'success': True, 'output_path': output_path, 'file_size': os.path.getsize(output_path)}


def _to_markdown(input_path: str, ext: str) -> dict:
    content = _read_text(input_path)
    output_path = unique_output_path('document', '.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return {'success': True, 'output_path': output_path, 'file_size': os.path.getsize(output_path)}


def _to_pdf(input_path: str, ext: str) -> dict:
    content = _read_text(input_path)
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
    except ImportError:
        return {'success': False, 'error': 'PDF conversion requires reportlab. Install with: pip install reportlab'}

    output_path = unique_output_path('document', '.pdf')
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    for line in content.split('\n'):
        if line.strip():
            story.append(Paragraph(line, styles['Normal']))
            story.append(Spacer(1, 6))
    doc.build(story)
    return {'success': True, 'output_path': output_path, 'file_size': os.path.getsize(output_path)}


def _to_docx(input_path: str, ext: str) -> dict:
    content = _read_text(input_path)
    try:
        from docx import Document
    except ImportError:
        return {'success': False, 'error': 'DOCX conversion requires python-docx. Install with: pip install python-docx'}

    doc = Document()
    for line in content.split('\n'):
        if line.strip():
            doc.add_paragraph(line)
    output_path = unique_output_path('document', '.docx')
    doc.save(output_path)
    return {'success': True, 'output_path': output_path, 'file_size': os.path.getsize(output_path)}
