# Generated by Django 2.2 on 2019-06-30 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0007_auto_20190630_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='is_teacher',
            field=models.BooleanField(default=False),
        ),
    ]
