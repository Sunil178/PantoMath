# Generated by Django 2.2.4 on 2019-08-18 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panto_math_app', '0002_auto_20190818_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
