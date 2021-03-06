# Generated by Django 3.0.8 on 2021-02-16 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ibursary_accounts', '0049_auto_20210215_1813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trialmodel',
            name='user',
        ),
        migrations.AddField(
            model_name='trialmodel',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='bursaryapplicant',
            name='last_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='trialmodel',
            name='first_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ann', to='ibursary_accounts.BursaryApplicant', to_field='first_name'),
        ),
        migrations.AlterField(
            model_name='trialmodel',
            name='last_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='njeri', to='ibursary_accounts.BursaryApplicant'),
        ),
        migrations.AlterField(
            model_name='trialmodel',
            name='middle_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_second_trialmodel', to=settings.AUTH_USER_MODEL),
        ),
    ]
