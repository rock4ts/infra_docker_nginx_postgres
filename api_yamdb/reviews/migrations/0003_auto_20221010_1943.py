# Generated by Django 2.2.16 on 2022-10-10 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20221010_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Год публикации'),
        ),
    ]
