# Generated by Django 5.2 on 2025-05-14 05:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0021_merge_20250514_0502"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UsersMockDjango",
            fields=[
                (
                    "user_id",
                    models.CharField(primary_key=True, serialize=False, unique=True),
                ),
                ("password", models.CharField()),
                ("phone", models.CharField()),
                ("zip", models.CharField()),
            ],
            options={
                "db_table": "users_mock",
            },
        ),
        migrations.CreateModel(
            name="UsersTable",
            fields=[
                (
                    "user_id",
                    models.CharField(primary_key=True, serialize=False, unique=True),
                ),
                ("password", models.CharField()),
                ("phone", models.CharField()),
                ("zip", models.CharField()),
            ],
            options={
                "db_table": "users_table",
            },
        ),
        migrations.CreateModel(
            name="FavoritesMockDjango",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "bill_id",
                    models.ForeignKey(
                        db_column="bill_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.billsmockdjango",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        db_column="user_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "favorites_mock",
                "unique_together": {("user_id", "bill_id")},
            },
        ),
        migrations.AlterField(
            model_name="favoritestable",
            name="user_id",
            field=models.ForeignKey(
                db_column="user_id",
                on_delete=django.db.models.deletion.CASCADE,
                to="core.userstable",
            ),
        ),
        migrations.DeleteModel(
            name="UserNotificationQueue",
        ),
    ]
