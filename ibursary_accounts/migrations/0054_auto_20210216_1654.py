# Generated by Django 3.0.8 on 2021-02-16 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibursary_accounts', '0053_auto_20210216_1651'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trialmodel',
            old_name='fname',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='trialmodel',
            old_name='lname',
            new_name='last_name',
        ),
        migrations.RenameField(
            model_name='trialmodel',
            old_name='mname',
            new_name='middle_name',
        ),
    ]