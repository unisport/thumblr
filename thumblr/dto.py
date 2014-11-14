class ImageMetadata(object):
    def __init__(self, file_name='',
                 site=None,
                 content_type=None,
                 object_id=None):
        self.original_file_name = file_name
        self.site = site
        self.content_type = content_type
        self.object_id = object_id
