from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password
from django.conf import settings
from random import randrange
from os import path


class ImageStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(ImageStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        raw_prefix, suffix = path.splitext(name)
        prefix = make_password(raw_prefix + str(randrange(10, 100000)))
        new_name = prefix + suffix
        return super(ImageStorage, self)._save(new_name, content)
