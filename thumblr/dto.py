class ImageMetadata(object):
    def __init__(self, file_name='',
                 site_id=None,
                 content_type=None,
                 object_id=None):
        self.original_file_name = file_name
        self.site_id = site_id
        self.content_type = content_type
        self.object_id = object_id
