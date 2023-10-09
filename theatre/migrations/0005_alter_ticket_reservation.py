# Generated by Django 4.1 on 2023-10-09 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("theatre", "0004_alter_reservation_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="reservation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="theatre.reservation",
            ),
        ),
    ]
