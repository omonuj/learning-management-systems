# Generated by Django 5.2 on 2025-05-02 23:53

import django.db.models.deletion
import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.FileField(blank=True, default='default.jpg', null=True, upload_to='categories/')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Category',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('tax_rate', models.IntegerField(default=5)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1000, null=True)),
                ('note', models.TextField()),
                ('note_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=22, max_length=20, prefix='', unique=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('review', models.TextField()),
                ('reply', models.CharField(blank=True, max_length=1000, null=True)),
                ('active', models.BooleanField(default=True)),
                ('ratings', models.IntegerField(choices=[('1', '1 Star'), ('2', '2 Star'), ('3', '3 Star'), ('4', '4 Star'), ('5', '5 Star')], default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('variant_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=22, max_length=20, prefix='', unique=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='VariantItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('variant_item_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=22, max_length=20, prefix='', unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('content_duration', models.CharField(blank=True, max_length=1000, null=True)),
                ('preview', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, default='files/default.jpg', null=True, upload_to='files/')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('introduction_video_file', models.FileField(blank=True, default='videos/default.mp4', null=True, upload_to='videos/')),
                ('image', models.ImageField(blank=True, default='images/default.jpg', null=True, upload_to='images/')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('language', models.CharField(choices=[('ENGLISH', 'English'), ('FRENCH', 'French'), ('SPANISH', 'Spanish')], default='ENGLISH', max_length=100)),
                ('level', models.CharField(choices=[('BEGINNER', 'Beginner'), ('INTERMEDIATE', 'Intermediate'), ('ADVANCED', 'Advanced')], default='BEGINNER', max_length=100)),
                ('platform_status', models.CharField(choices=[('REVIEW', 'Review'), ('DISABLED', 'Disabled'), ('REJECTED', 'Rejected'), ('DRAFT', 'Draft'), ('PUBLISHED', 'Published')], default='PUBLISHED', max_length=100)),
                ('teacher_course_status', models.CharField(choices=[('DRAFT', 'Draft'), ('DISABLED', 'Disabled'), ('PUBLISHED', 'Published')], default='PUBLISHED', max_length=100)),
                ('featured', models.BooleanField(default=False)),
                ('course_id', shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', length=6, max_length=20, prefix='', unique=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.category')),
            ],
        ),
    ]
