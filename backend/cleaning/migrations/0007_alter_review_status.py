# Generated by Django 5.1.6 on 2025-03-02 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cleaning", "0006_alter_cleaning_status_alter_review_status"),
    ]

    operations = [
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
