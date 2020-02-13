from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Convocatoria


class ConvocatoriaAdmin(ImportExportModelAdmin):
    # fields = ['*',]
    search_fields = ('cuce', 'entidad', 'objetoContratación', 'estado', 'fechaPresentación', 'fechaPublicación', 'personaContacto', 'garantía', 'costoPliego', 'arpc', 'reuniónAclaración', 'fechaAdjudicaciónDesierta', 'departamento', 'normativa')
    list_filter = ('modalidad', 'estado', 'montoContrato', 'fechaPresentación', 'fechaPublicación', 'garantía', 'costoPliego', 'arpc', 'reuniónAclaración', 'fechaAdjudicaciónDesierta', 'departamento', 'normativa')
    list_display = ('cuce', 'entidad', 'modalidad', 'objetoContratación', 'estado', 'montoContrato', 'fechaPresentación', 'fechaPublicación', 'personaContacto', 'garantía', 'costoPliego', 'arpc', 'reuniónAclaración', 'fechaAdjudicaciónDesierta', 'departamento', 'normativa')

admin.site.register(Convocatoria, ConvocatoriaAdmin)
#'cuce', 'entidad', 'modalidad', 'objetoContratación', 'estado', 'montoContrato',, 'fechaPresentación', 'fechaPublicación', 'archivos', 'formularios', 'personaContacto', 'garantía', 'costoPliego', 'arpc', 'reuniónAclaración', 'fechaAdjudicaciónDesierta', 'departamento', 'normativa'
