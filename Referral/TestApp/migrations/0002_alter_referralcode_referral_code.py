# Generated by Django 4.0.4 on 2022-06-07 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referralcode',
            name='referral_code',
            field=models.CharField(max_length=8),
        ),
    ]