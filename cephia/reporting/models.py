# # encoding: utf-8
# from django.db import models
# import logging
# from django.conf import settings

# logger = logging.getLogger(__name__)

# class Report(models.Model):
#     class Meta:
#         db_table = "cephia_reports"

#     name = models.CharField(max_length=255, null=False, blank=False)
#     description = models.TextField(null=True)
#     query = models.TextField(null=False, blank=False)
#     created = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

#     def __unicode__(self):
#         return "%s" % (self.name)
