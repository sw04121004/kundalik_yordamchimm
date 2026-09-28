# backend/apps/ai/storage.py
"""Helper utilities for storing uploaded media files.

The project currently stores media locally under a ``media/`` directory at the project root.
If you later want to switch to a cloud bucket (e.g., S3), replace the implementation of
``save_media`` accordingly.
"""
import os
import uuid
from pathlib import Path
from django.conf import settings

# Ensure the MEDIA_ROOT exists – if not, create it.
MEDIA_ROOT = getattr(settings, "MEDIA_ROOT", None)
if not MEDIA_ROOT:
    # Fallback: create a ``media`` folder next to the project base.
    BASE_DIR = Path(__file__).resolve().parents[3]
    MEDIA_ROOT = BASE_DIR / "media"
    os.makedirs(MEDIA_ROOT, exist_ok=True)

def save_media(file_obj) -> str:
    """Save an uploaded ``file_obj`` (InMemoryUploadedFile or TemporaryUploadedFile).

    Returns a URL that can be used to serve the file via Django's ``MEDIA_URL``.
    The function generates a UUID‑based filename to avoid collisions.
    """
    # Preserve original extension
    ext = Path(file_obj.name).suffix
    filename = f"{uuid.uuid4().hex}{ext}"
    destination = Path(MEDIA_ROOT) / filename

    # Write the file content to disk
    with open(destination, "wb") as out_file:
        for chunk in file_obj.chunks():
            out_file.write(chunk)

    # Build the public URL – settings.MEDIA_URL must end with a trailing slash.
    media_url = getattr(settings, "MEDIA_URL", "/media/")
    return f"{media_url}{filename}"
