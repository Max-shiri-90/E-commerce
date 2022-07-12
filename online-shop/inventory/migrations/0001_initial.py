# Generated by Django 4.0.4 on 2022-05-28 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.category')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureKey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255)),
                ('category', models.ManyToManyField(to='inventory.category')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('feature_key', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='inventory.featurekey')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('product_price', models.FloatField()),
                ('rate', models.FloatField(blank=True, null=True)),
                ('total_quantity', models.IntegerField()),
                ('available_quantity', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField()),
                ('image', models.ImageField(default='default.jpg', upload_to='Products/')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('discount_price', models.FloatField(blank=True, null=True)),
                ('discount_percentage', models.FloatField(default=0)),
                ('added_date', models.DateField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='inventory.category')),
                ('feature_value', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='inventory.featurevalue')),
                ('supplier', models.ManyToManyField(to='accounts.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=5000)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('user_rate', models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=10, null=True)),
                ('commenting_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.customer')),
                ('product', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='inventory.product')),
            ],
        ),
    ]