# Generated by Django 2.1.7 on 2019-03-20 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('etiquetas', '0008_auto_20190313_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destinatario',
            name='id_remetente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='etiquetas.Remetente'),
        ),
    ]
