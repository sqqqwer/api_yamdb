# Generated by Django 3.2 on 2024-11-17 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yamdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='Биография'),
        ),
    ]
