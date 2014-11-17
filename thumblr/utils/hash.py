import hashlib


def file_hash(content=None):
    if content is None:
        return None
    md5 = hashlib.md5()
    for chunk in content.chunks():
        md5.update(chunk)
    return md5.hexdigest()[:12]
