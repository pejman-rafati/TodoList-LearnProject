# Generated by Django 5.0.2 on 2024-02-17 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0010_alter_task_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('F', 'Free'), ('P', 'Pro')], default='F', max_length=1),
        ),
    ]
