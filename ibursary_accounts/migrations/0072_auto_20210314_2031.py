# Generated by Django 3.0.8 on 2021-03-14 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ibursary_accounts', '0071_auto_20210314_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trialmodel',
            name='first_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ibursary_accounts.BursaryApplicant'),
        ),
    ]