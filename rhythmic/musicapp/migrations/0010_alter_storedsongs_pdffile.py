# Generated by Django 4.2.19 on 2025-03-15 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicapp', '0009_rename_created_at_storedsongs_createdat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storedsongs',
            name='pdfFile',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
