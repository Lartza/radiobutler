import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from PIL import Image


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        """Returns a filename that's free on the target storage system, and available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class LogoStorage(OverwriteStorage):

    def _save(self, name, content):
        parent_return = super()._save(name, content)

        # Hack to resize and save the logo to the required sizes
        image = Image.open(content)
        for size in [(32, 32), (112, 32), (128, 128), (320, 240)]:
            image_resized = image.resize(size)
            image_resized.save(self.path(name).replace('.png', f'_{size[0]}.png'), 'PNG')

        return parent_return
