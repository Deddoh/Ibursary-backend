# Generated by Django 3.0.8 on 2021-02-16 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ibursary_accounts', '0050_auto_20210216_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trialmodel',
            name='middle_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_second_trialmodel', to='ibursary_accounts.BursaryApplicant'),
        ),
    ]
