# Generated by Django 3.0.8 on 2020-10-23 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibursary_accounts', '0009_submittedapplicationsmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submittedapplicationsmodel',
            name='creation_date',
            field=models.CharField(max_length=100),
        ),
    ]
