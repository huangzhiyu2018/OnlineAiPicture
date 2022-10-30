# Generated by Django 4.1.2 on 2022-10-30 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("picturerec", "0013_studentsinfor"),
    ]

    operations = [
        migrations.CreateModel(
            name="PersonInfor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        default="",
                        max_length=125,
                        upload_to="persons/",
                        verbose_name="文件",
                    ),
                ),
                ("person_name", models.CharField(max_length=30, verbose_name="姓名")),
                ("create_time", models.DateField(verbose_name="上传时间")),
                ("upload_user", models.CharField(max_length=30, verbose_name="上传者")),
            ],
        ),
    ]
