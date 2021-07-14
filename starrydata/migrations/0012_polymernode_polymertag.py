# Generated by Django 3.2.4 on 2021-07-12 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('starrydata', '0011_auto_20210630_0813'),
    ]

    operations = [
        migrations.CreateModel(
            name='PolymerTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PolymerNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='starrydata.polymernode')),
                ('polymer_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='starrydata.polymertag')),
            ],
        ),
    ]