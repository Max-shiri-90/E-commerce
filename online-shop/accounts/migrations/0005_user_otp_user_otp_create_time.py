# Generated by Django 4.0.4 on 2022-06-16 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_address_alley_remove_address_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='otp_create_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
