# Generated by Django 4.1.2 on 2022-10-11 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserInfor",
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
                ("userName", models.CharField(max_length=30, verbose_name="用户名")),
                ("passWord", models.CharField(max_length=80, verbose_name="密码")),
                ("powerRights", models.CharField(max_length=30, verbose_name="权重")),
            ],
        ),
    ]
