# Generated by Django 3.0.8 on 2021-03-19 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ibursary_accounts', '0077_auto_20210319_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trialmodel',
            name='Model_Recommendation',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
