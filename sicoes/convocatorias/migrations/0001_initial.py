# Generated by Django 2.2.3 on 2019-07-22 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Convocatoria',
            fields=[
                ('cuce', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('entidad', models.CharField(max_length=100)),
                ('modalidad', models.CharField(max_length=5)),
                ('objetoContratación', models.CharField(max_length=640)),
                ('estado', models.CharField(max_length=14)),
                ('montoContrato', models.IntegerField()),
                ('fechaPresentación', models.DateField()),
                ('fechaPublicación', models.DateField()),
                ('archivos', models.TextField()),
                ('formularios', models.TextField()),
                ('personaContacto', models.CharField(max_length=250)),
                ('garantía', models.CharField(max_length=255, null=True)),
                ('costoPliego', models.IntegerField(null=True)),
                ('arpc', models.CharField(max_length=10)),
                ('reuniónAclaración', models.DateTimeField(null=True)),
                ('fechaAdjudicaciónDesierta', models.DateField(null=True)),
                ('departamento', models.CharField(max_length=15)),
                ('normativa', models.CharField(max_length=5)),
            ],
        ),
    ]
