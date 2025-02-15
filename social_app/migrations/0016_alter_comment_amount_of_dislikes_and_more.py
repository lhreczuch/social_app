# Generated by Django 5.0.3 on 2024-03-17 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0015_alter_post_image_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='amount_of_dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='amount_of_likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='post_pics/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
