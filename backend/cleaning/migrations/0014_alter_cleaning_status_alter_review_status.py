# Generated by Django 5.1.6 on 2025-03-02 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cleaning", "0013_cleaning_arrival_time_cleaning_departure_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cleaning",
            name="status",
            field=models.CharField(
                choices=[("P", "pending"), ("C", "completed"), ("A", "assigned")],
                default="P",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="status",
            field=models.CharField(
                choices=[("N", "not_checked"), ("C", "checked"), ("I", "issue_found")],
                default="N",
                max_length=1,
            ),
        ),
    ]
