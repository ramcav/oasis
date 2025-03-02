# Generated by Django 5.1.6 on 2025-03-02 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cleaning", "0008_alter_cleaning_status_alter_review_handyman_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cleaning",
            name="status",
            field=models.CharField(
                choices=[("C", "completed"), ("P", "pending"), ("A", "assigned")],
                default="P",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="review",
            name="status",
            field=models.CharField(
                choices=[("N", "not_checked"), ("I", "issue_found"), ("C", "checked")],
                default="N",
                max_length=1,
            ),
        ),
    ]
