# Generated by Django 2.1.7 on 2019-03-11 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etiquetas', '0004_etiqueta_data_gerado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etiqueta',
            name='data_gerado',
            field=models.DateTimeField(null=True),
        ),
    ]