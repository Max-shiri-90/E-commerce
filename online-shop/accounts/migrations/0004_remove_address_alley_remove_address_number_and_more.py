# Generated by Django 4.0.4 on 2022-06-16 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_address_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='alley',
        ),
        migrations.RemoveField(
            model_name='address',
            name='number',
        ),
        migrations.RemoveField(
            model_name='address',
            name='street',
        ),
    ]
