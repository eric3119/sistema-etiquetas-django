# Generated by Django 2.1.7 on 2019-03-13 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('etiquetas', '0006_auto_20190313_1422'),
    ]

    operations = [
        migrations.RenameField(
            model_name='destinatario',
            old_name='id_destinatario',
            new_name='id_rementente',
        ),
    ]
