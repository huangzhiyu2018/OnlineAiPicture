# Generated by Django 4.1.2 on 2022-10-11 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("picturerec", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TrainSet",
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
                ("featurename", models.CharField(max_length=30, verbose_name="特征名")),
                ("targetname", models.CharField(max_length=30, verbose_name="标签名")),
                ("imagesize", models.CharField(max_length=30, verbose_name="图片大小名")),
                ("truename", models.CharField(max_length=30, verbose_name="真实标签名")),
            ],
        ),
        migrations.AlterField(
            model_name="userinfor",
            name="powerRights",
            field=models.CharField(
                choices=[("管理员", "管理员"), ("用户", "用户")], max_length=30, verbose_name="权重"
            ),
        ),
    ]
