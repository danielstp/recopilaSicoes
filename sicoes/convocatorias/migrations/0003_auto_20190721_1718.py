# Generated by Django 2.2.3 on 2019-07-21 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convocatorias', '0002_auto_20190721_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convocatoria',
            name='arpc',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='convocatoria',
            name='departamento',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='convocatoria',
            name='garantía',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='convocatoria',
            name='normativa',
            field=models.CharField(max_length=5),
        ),
    ]
