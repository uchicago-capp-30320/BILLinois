# Generated by Django 5.2 on 2025-05-12 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_actionstable_chamber"),
    ]

    operations = [
        migrations.AddField(
            model_name="billsmockdjango",
            name="session",
            field=models.CharField(default=None, null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="billsmockdjango",
            name="state",
            field=models.CharField(default=None, null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="billstable",
            name="session",
            field=models.CharField(default=None, null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="billstable",
            name="state",
            field=models.CharField(default=None, null=True),
            preserve_default=False,
        ),
    ]
