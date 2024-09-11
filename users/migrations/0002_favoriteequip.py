# Generated by Django 4.2.10 on 2024-09-11 04:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0002_equipment_loan_status'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteEquip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('equip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment.equipment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorite',
                'unique_together': {('user', 'equip')},
            },
        ),
    ]
