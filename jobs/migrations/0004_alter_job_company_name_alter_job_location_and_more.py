# Generated by Django 4.0.4 on 2022-05-18 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_alter_job_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='company_name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='job',
            name='seniority',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='job',
            name='title',
            field=models.CharField(max_length=250),
        ),
    ]
