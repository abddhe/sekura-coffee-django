# Generated by Django 4.1.7 on 2023-03-14 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0006_order_canceled"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="user_token",
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
    ]
