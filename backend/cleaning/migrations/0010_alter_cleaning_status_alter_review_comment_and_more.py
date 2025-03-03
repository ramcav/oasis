# Generated by Django 5.1.6 on 2025-03-02 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cleaning", "0009_alter_cleaning_status_alter_review_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cleaning",
            name="status",
            field=models.CharField(
                choices=[("A", "assigned"), ("C", "completed"), ("P", "pending")],
                default="P",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="comment",
            field=models.CharField(blank=True, max_length=200),
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
