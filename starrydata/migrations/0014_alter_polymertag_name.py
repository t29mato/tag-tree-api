# Generated by Django 3.2.4 on 2021-07-12 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('starrydata', '0013_alter_polymertagtreenode_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polymertag',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
