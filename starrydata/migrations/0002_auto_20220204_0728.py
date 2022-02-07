# Generated by Django 3.1.8 on 2022-02-04 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('starrydata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='synonyms',
            field=models.ManyToManyField(blank=True, related_name='_tag_synonyms_+', to='starrydata.Tag'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=64),
        ),
    ]