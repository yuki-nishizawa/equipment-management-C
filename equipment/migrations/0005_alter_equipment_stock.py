# Generated by Django 4.2.10 on 2024-09-13 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='stock',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
