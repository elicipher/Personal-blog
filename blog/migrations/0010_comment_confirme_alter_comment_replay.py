# Generated by Django 5.1.7 on 2025-04-09 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_postvisit_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='confirme',
            field=models.BooleanField(default=False, verbose_name='تایید شده'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='replay',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.comment', verbose_name='پاسخ'),
        ),
    ]
