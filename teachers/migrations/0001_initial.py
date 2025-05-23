# Generated by Django 5.2 on 2025-05-02 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('active', models.BooleanField(default=False)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, default='default.jpg', null=True, upload_to='teachers/')),
                ('full_name', models.CharField(max_length=100)),
                ('bio', models.TextField()),
                ('facebook', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('about', models.TextField()),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
