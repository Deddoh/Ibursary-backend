# Generated by Django 3.0.8 on 2021-02-11 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ibursary_accounts', '0039_auto_20210211_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trialmodel',
            name='chief',
        ),
    ]
