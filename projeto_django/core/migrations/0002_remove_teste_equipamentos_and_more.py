# Generated by Django 5.1.2 on 2024-10-23 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teste',
            name='equipamentos',
        ),
        migrations.RemoveField(
            model_name='teste',
            name='om_responsavel',
        ),
        migrations.AddField(
            model_name='usuario',
            name='nome',
            field=models.CharField(default='Sem Nome', max_length=255),
        ),
        migrations.AlterField(
            model_name='teste',
            name='data_fim',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='teste',
            name='data_inicio',
            field=models.DateTimeField(),
        ),
    ]
