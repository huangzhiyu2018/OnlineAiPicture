# Generated by Django 4.1.2 on 2022-10-21 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("picturerec", "0011_rename_picture_id_recogresult_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recogresult",
            name="picture",
            field=models.CharField(default="", max_length=125, verbose_name="图片ID列表"),
        ),
    ]
