# Generated by Django 2.2.3 on 2019-07-23 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convocatorias', '0004_auto_20190722_0155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convocatoria',
            name='fechaPublicación',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='convocatoria',
            name='objetoContratación',
            field=models.TextField(),
        ),
    ]
