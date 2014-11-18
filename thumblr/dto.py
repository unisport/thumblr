class ImageMetadata(object):
    def __init__(self, file_name='',
                 site_id=None,
                 size_slug=None,
                 content_type_id=None,
                 object_id=None):
        self.original_file_name = file_name
        self.site_id = site_id
        self.content_type_id = content_type_id
        self.object_id = object_id
        self.size_slug = size_slug


class ImageUrlSpec(object):
    S3_URL = 's3'
    CDN_URL = 'cdn'
    PATH_ONLY_URL = 'path'