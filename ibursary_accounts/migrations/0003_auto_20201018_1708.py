# Generated by Django 3.0.8 on 2020-10-18 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibursary_accounts', '0002_auto_20201018_1647'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bursaryapplicant',
            old_name='ID_Number',
            new_name='ID_number',
        ),
    ]