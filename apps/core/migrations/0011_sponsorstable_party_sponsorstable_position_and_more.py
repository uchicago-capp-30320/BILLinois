# Generated by Django 5.2 on 2025-04-29 22:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0010_billstable_userstable_actionstable_sponsorstable_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="sponsorstable",
            name="party",
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name="sponsorstable",
            name="position",
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name="actionstable",
            name="category",
            field=models.CharField(null=True),
        ),
        migrations.AlterField(
            model_name="sponsorstable",
            name="sponsor_id",
            field=models.CharField(null=True),
        ),
    ]
