from django.db import models
from django.forms.models import model_to_dict as _model_to_dict
from datetime import datetime

class BaseModel(models.Model):
    class Meta:
        abstract=True
        default_permissions = []

    created = models.DateTimeField()
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.modified = datetime.now()
        if self.id is None:
            self.created = self.modified
        super(BaseModel, self).save(*args, **kwargs)
    
    def model_to_dict(self):
        return model_to_dict_with_date_support(self)
