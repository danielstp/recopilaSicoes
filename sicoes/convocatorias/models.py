from django.db import models

class Convocatoria(models.Model):
    cuce = models.CharField(max_length=25, primary_key=True)
    entidad = models.CharField(max_length=100)
    modalidad = models.CharField(max_length=5)
    objetoContratación = models.CharField(max_length=640)
    estado = models.CharField(max_length=14)
    montoContrato = models.IntegerField()
    fechaPresentación = models.DateField()
    fechaPublicación = models.DateField()
    archivos = models.TextField()
    formularios = models.TextField()
    personaContacto = models.CharField(max_length=250)
    garantía = models.CharField(max_length=100)
    costoPliego = models.IntegerField(null=True)
    arpc = models.CharField(max_length=10)
    reuniónAclaración = models.DateTimeField(null=True,blank=True)
    fechaAdjudicaciónDesierta = models.DateField(null=True,blank=True)
    departamento = models.CharField(max_length=15)
    normativa = models.CharField(max_length=5)

    def __str__(self):
        return self.cuce
