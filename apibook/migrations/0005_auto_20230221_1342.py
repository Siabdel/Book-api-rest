# Generated by Django 3.2.15 on 2023-02-21 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apibook', '0004_paramtimerprayer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paramtimerprayer',
            options={'ordering': ['ville']},
        ),
        migrations.AlterUniqueTogether(
            name='paramtimerprayer',
            unique_together={('ville',)},
        ),
    ]
