# Generated by Django 5.2.3 on 2025-07-07 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='stripe_charge_id',
        ),
        migrations.AddField(
            model_name='payment',
            name='from_balance',
            field=models.BooleanField(default=False),
        ),
    ]
