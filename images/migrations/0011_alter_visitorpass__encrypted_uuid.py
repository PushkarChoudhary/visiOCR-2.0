# Generated by Django 5.1.2 on 2024-11-24 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0010_rename_uuid_visitorpass__encrypted_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitorpass',
            name='_encrypted_uuid',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
