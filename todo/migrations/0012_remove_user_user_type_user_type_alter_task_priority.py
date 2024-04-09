# Generated by Django 5.0.2 on 2024-02-17 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0011_user_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_type',
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('P', 'Pro'), ('A', 'Admin'), ('F', 'Free')], default='F', max_length=1),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('M', 'Medium'), ('H', 'High'), ('L', 'Low')], default='L', max_length=1),
        ),
    ]
