# Generated by Django 2.0.1 on 2018-03-11 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_classquizresults_answerset'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classquizresults',
            name='answerset',
        ),
    ]
