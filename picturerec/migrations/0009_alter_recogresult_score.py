# Generated by Django 4.1.2 on 2022-10-19 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("picturerec", "0008_recogresult_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recogresult",
            name="score",
            field=models.TextField(blank=True, null=True, verbose_name="评估值"),
        ),
    ]
