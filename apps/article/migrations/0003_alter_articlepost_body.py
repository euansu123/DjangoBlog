# Generated by Django 5.0.7 on 2025-05-10 16:46

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("article", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="articlepost",
            name="body",
            field=ckeditor_uploader.fields.RichTextUploadingField(
                verbose_name="文章内容"
            ),
        ),
    ]
