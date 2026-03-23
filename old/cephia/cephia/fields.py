from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class ProtectedForeignKey(models.ForeignKey):

    def __init__(self, *args, **kwargs):
        kwargs['on_delete'] = models.PROTECT
        super(ProtectedForeignKey, self).__init__(*args, **kwargs)
