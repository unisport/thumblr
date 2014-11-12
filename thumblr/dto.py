class ImageMetadataDTO(object):
    def __init__(self, file_name='', file_type=None,
                 site_id=None, content_type_id=None,
                 object_id=None):

        self.file_name = file_name
        self.file_type = file_type

        self.site_id = site_id

        self.content_type_id = content_type_id
        self.object_id = object_id
