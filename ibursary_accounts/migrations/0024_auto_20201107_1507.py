# Generated by Django 3.0.8 on 2020-11-07 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibursary_accounts', '0023_auto_20201105_1636'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submittedapplicationsmodel',
            old_name='first_name',
            new_name='user',
        ),
    ]
