from django.apps import AppConfig


class AssayConfig(AppConfig):
    name = 'assay'
    verbose_name = "Assay"

    def ready(self):
        from assay_result_factory import register_result_model, register_result_row_model
        from models import *

        register_result_model(ArchitectAvidityResult, 'ArchitectAvidity')
        register_result_model(ArchitectUnmodifiedResult, 'ArchitectUnmodified')
        register_result_model(BEDResult, 'BED')
        register_result_model(BioRadAvidityCDCResult, 'BioRadAvidity-CDC')
        register_result_model(BioRadAvidityGlasgowResult, 'BioRadAvidity-Glasgow')
        register_result_model(BioRadAvidityJHUResult, 'BioRadAvidity-JHU')
        register_result_model(GeeniusResult, 'Geenius')
        register_result_model(IDEV3Result, 'IDE-V3')
        register_result_model(LagMaximResult, 'LAg-Maxim')
        register_result_model(LagSediaResult, 'LAg-Sedia')
        register_result_model(LSVitrosDiluentResult, 'LSVitros-Diluent')
        register_result_model(LSVitrosPlasmaResult, 'LSVitros-Plasma')
        register_result_model(LuminexCDCResult, 'BioPlex-CDC')
        register_result_model(VitrosAvidityResult, 'Vitros')
        register_result_model(ISGlobalResult, 'ISGlobal')

        register_result_row_model(ArchitectAvidityResultRow, 'ArchitectAvidity')
        register_result_row_model(ArchitectUnmodifiedResultRow, 'ArchitectUnmodified')
        register_result_row_model(BEDResultRow, 'BED')
        register_result_row_model(BioRadAvidityCDCResultRow, 'BioRadAvidity-CDC')
        register_result_row_model(BioRadAvidityGlasgowResultRow, 'BioRadAvidity-Glasgow')
        register_result_row_model(BioRadAvidityJHUResultRow, 'BioRadAvidity-JHU')
        register_result_row_model(GeeniusResultRow, 'Geenius')
        register_result_row_model(IDEV3ResultRow, 'IDE-V3')
        register_result_row_model(LagMaximResultRow, 'LAg-Maxim')
        register_result_row_model(LagSediaResultRow, 'LAg-Sedia')
        register_result_row_model(LSVitrosDiluentResultRow, 'LSVitros-Diluent')
        register_result_row_model(LSVitrosPlasmaResultRow, 'LSVitros-Plasma')
        register_result_row_model(LuminexCDCResultRow, 'BioPlex-CDC')
        register_result_row_model(VitrosAvidityResultRow, 'Vitros')
        register_result_row_model(ISGlobalResultRow, 'ISGlobal')
