# Generated by Django 4.1.7 on 2023-08-17 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_alter_entry_project_alter_entry_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('archived', 'Archived')], default='active', max_length=20),
        ),
    ]
