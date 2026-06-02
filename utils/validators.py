import os
from config import Config
from services.format_registry import get_category_for_extension, is_valid_output_format


def validate_file_size(file_storage) -> tuple[bool, str]:
    file_storage.seek(0, 2)
    size = file_storage.tell()
    file_storage.seek(0)
    if size > Config.MAX_CONTENT_LENGTH:
        mb = Config.MAX_CONTENT_LENGTH // (1024 * 1024)
        return False, f"File too large. Maximum {mb}MB"
    if size == 0:
        return False, "File is empty"
    return True, ""


def validate_input_file(filename: str) -> tuple[bool, str]:
    ext = os.path.splitext(filename)[1].lower()
    if not ext:
        return False, "File has no extension"
    category = get_category_for_extension(ext)
    if not category:
        return False, f"Unsupported file format: {ext}"
    return True, category['id']


def validate_output(category_id: str, output_format: str) -> tuple[bool, str]:
    if not is_valid_output_format(category_id, output_format):
        return False, f"Format '{output_format}' is not valid for this file type"
    return True, ""
