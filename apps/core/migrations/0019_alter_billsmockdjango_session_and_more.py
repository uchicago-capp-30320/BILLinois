# Generated by Django 5.2 on 2025-05-13 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0018_rename_bill_session_billsmockdjango_session_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="billsmockdjango",
            name="session",
            field=models.CharField(default='session: "104th"'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="billsmockdjango",
            name="state",
            field=models.CharField(default="IL"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="billstable",
            name="session",
            field=models.CharField(default='session: "104th"'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="billstable",
            name="state",
            field=models.CharField(default="IL"),
            preserve_default=False,
        ),
    ]
