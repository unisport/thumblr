from django.core.files import File

from thumblr.utils.hash import file_hash


class HashedFile(File):
    def __init__(self, file, name=None):
        super(HashedFile, self).__init__(file, name)
        self.name = file_hash(self)
