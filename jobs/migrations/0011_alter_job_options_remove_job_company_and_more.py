# Generated by Django 4.0.4 on 2022-05-24 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_alter_job_options_remove_job_company_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={},
        ),
        migrations.RemoveField(
            model_name='job',
            name='company',
        ),
        migrations.AddField(
            model_name='job',
            name='company_name',
            field=models.CharField(default=None, max_length=250),
        ),
    ]
