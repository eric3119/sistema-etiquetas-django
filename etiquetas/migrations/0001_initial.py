# Generated by Django 2.1.7 on 2019-03-11 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('funcao', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('orgao', models.CharField(max_length=100)),
                ('endereco', models.CharField(max_length=100)),
            ],
        ),
    ]