# Generated by Django 4.0.5 on 2022-06-21 07:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0004_alter_razorpayorderid_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='razorpayorderid',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='razorpayorderid',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='razorpayorderid',
            name='amount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='razorpayorderid',
            name='amount_due',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='razorpayorderid',
            name='amount_paid',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='razorpayorderid',
            name='merchant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='merchant', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='razorpayorderid',
            name='notes1',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='razorpayorderid',
            name='notes2',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='razorpayorderid',
            name='order_id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='razorpayorderid',
            name='status',
            field=models.CharField(max_length=255),
        ),
    ]