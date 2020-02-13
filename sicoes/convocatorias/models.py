from django.db import models


class Convocatoria(models.Model):
    cuce = models.CharField(max_length=25, primary_key=True)
    entidad = models.CharField(max_length=251)
    modalidad = models.CharField(max_length=5)
    objetoContratación = models.TextField("Objeto de Contratación")
    estado = models.CharField(max_length=48)
    montoContrato = models.DecimalField("Monto Contrato en Bs.", default=0, decimal_places=2, max_digits=20)
    fechaPresentación = models.DateField("Fecha Presentación", null=True)
    fechaPublicación = models.DateField("Fecha Publicación", null=True)
    archivos = models.TextField()
    formularios = models.TextField()
    personaContacto = models.CharField("Persona de Contacto", max_length=250)
    garantía = models.CharField(max_length=255,null=True)
    costoPliego = models.DecimalField("Costo Pliego", null=True, default=0, decimal_places=2, max_digits=20)
    arpc = models.CharField(max_length=10)
    reuniónAclaración = models.DateTimeField("Fecha de la Reunión de Aclaración", null=True)
    fechaAdjudicaciónDesierta = models.DateField(null=True)
    departamento = models.CharField(max_length=15)
    normativa = models.CharField(max_length=150)

    def __str__(self):
        return self.cuce
