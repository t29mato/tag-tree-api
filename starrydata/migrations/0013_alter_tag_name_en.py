# Generated by Django 3.2.4 on 2021-07-26 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('starrydata', '0012_auto_20210726_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name_en',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
