# Generated by Django 4.2.4 on 2023-08-12 23:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='urlmapping',
            options={'ordering': ['-created']},
        ),
    ]
