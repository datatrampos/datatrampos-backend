# Generated by Django 4.0.4 on 2023-01-11 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_alter_company_glassdoor_alter_company_linkedin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='company',
            name='haveOpenings',
            field=models.BooleanField(default=False),
        ),
    ]