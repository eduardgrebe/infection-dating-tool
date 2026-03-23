from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import ReverseOneToOneDescriptor
class ProtectedForeignKey(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        kwargs['on_delete'] = models.PROTECT
        super(ProtectedForeignKey, self).__init__(*args, **kwargs)

class SingleRelatedObjectDescriptorReturnsNone(ReverseOneToOneDescriptor):
    def __get__(self, instance, instance_type=None):
        try:
            return super(SingleRelatedObjectDescriptorReturnsNone, self).__get__(instance=instance, instance_type=instance_type)
        except ObjectDoesNotExist:
            return None

class OneToOneOrNoneField(models.OneToOneField):
    """A OneToOneField that returns None if the related object doesn't exist"""
    related_accessor_class = SingleRelatedObjectDescriptorReturnsNone

try:
    from imagekit.models import ImageSpecField
    from imagekit.processors import ResizeToFill
except ImportError:
    pass
else:
    class ThumbnailField(ImageSpecField):
        def __init__(self, source, *args, **kwargs):
            kwargs['processors'] = [ResizeToFill(100, 50)]
            kwargs['format'] = 'JPEG'
            kwargs['options'] = {'quality': 90}

            super(ThumbnailField, self).__init__(source=source, *args, **kwargs)

