# Generated by Django 4.1.7 on 2023-04-18 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_entry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]