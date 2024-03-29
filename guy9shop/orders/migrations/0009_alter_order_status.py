# Generated by Django 4.2.7 on 2024-03-16 17:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0008_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("processing", "Processing"),
                    ("paid", "Paid"),
                    ("shipped", "Shipped"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
    ]
