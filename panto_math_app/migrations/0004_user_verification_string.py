# Generated by Django 2.2.4 on 2019-09-01 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panto_math_app', '0003_auto_20190818_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verification_string',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
