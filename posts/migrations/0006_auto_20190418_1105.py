# Generated by Django 2.1.7 on 2019-04-18 02:05

from django.db import migrations, models
import django.utils.timezone
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to=''),
        ),
    ]