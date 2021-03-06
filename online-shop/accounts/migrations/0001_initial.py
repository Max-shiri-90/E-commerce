# Generated by Django 4.0.4 on 2022-05-28 20:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator('^09\\d{9}$')])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'auth_user',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bank_info', models.CharField(blank=True, max_length=250, null=True)),
                ('joined_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Customer',
            },
            bases=('accounts.user',),
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bank_info', models.CharField(blank=True, max_length=250, null=True)),
                ('company_name', models.CharField(max_length=100)),
                ('joined_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Supplier',
            },
            bases=('accounts.user',),
        ),
        migrations.CreateModel(
            name='CustomerWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_info', models.CharField(max_length=250)),
                ('credit', models.CharField(max_length=250)),
                ('payment_info', models.JSONField(verbose_name={})),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('province', models.CharField(max_length=255, verbose_name='??????????')),
                ('city', models.CharField(max_length=255, verbose_name='??????')),
                ('street', models.CharField(max_length=255, verbose_name='????????????')),
                ('alley', models.CharField(max_length=255, verbose_name='????????')),
                ('number', models.CharField(max_length=255, verbose_name='????????')),
                ('customer_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
            options={
                'verbose_name': 'Address',
            },
            bases=('accounts.user',),
        ),
    ]
