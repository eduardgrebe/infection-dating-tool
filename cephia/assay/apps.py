from django.apps import AppConfig


class AssayConfig(AppConfig):
    name = 'assay'
    verbose_name = "Assay"

    def ready(self):
        from assay_result_factory import *
