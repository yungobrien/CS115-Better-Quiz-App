# Generated by Django 2.0.1 on 2018-03-11 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20180310_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='classquizresults',
            name='answerset',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='polls.AnswerSet'),
        ),
    ]
