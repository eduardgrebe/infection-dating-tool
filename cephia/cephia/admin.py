from django.contrib import admin
from models import (Country, FileInfo, SubjectRow, Subject, Ethnicity, Visit,
                    VisitRow, Site, Specimen, SpecimenType, TransferInRow,
                    Study, TransferOutRow, AliquotRow)

admin.site.register(Country)
admin.site.register(FileInfo)
admin.site.register(SubjectRow)
admin.site.register(Subject)
admin.site.register(Ethnicity)
admin.site.register(Visit)
admin.site.register(VisitRow)
admin.site.register(Site)
admin.site.register(Specimen)
admin.site.register(SpecimenType)
admin.site.register(TransferInRow),
admin.site.register(Study)
admin.site.register(TransferOutRow)
admin.site.register(AliquotRow)
