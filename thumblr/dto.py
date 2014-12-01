__all__ = ['ImageMetadata', 'ImageUrlSpec']


class ImageMetadata(object):
    """
    This should be used everywhere, it abstracts data model. In perfect world, orm models like
    Image and ImageFile should never go out of thumblr application and appear anywhere else.
    """

    def __init__(self,
                 image_file_id=None,
                 image_hash=None,

                 file_name=None,
                 site_id=None,
                 size_slug=None,
                 content_type_id=None,
                 object_id=None):
        self.image_file_id = image_file_id
        self.image_hash = image_hash

        self.original_file_name = file_name
        self.site_id = site_id
        self.content_type_id = content_type_id
        self.object_id = object_id
        self.size_slug = size_slug

    def __str__(self):
        return "{image_file_id}::{file_name}::{size}".format(
            image_file_id=self.image_file_id,
            file_name=self.original_file_name,
            size=self.size_slug,
        )


class ImageUrlSpec(object):
    S3_URL = 's3'
    CDN_URL = 'cdn'
    PATH_ONLY_URL = 'path'