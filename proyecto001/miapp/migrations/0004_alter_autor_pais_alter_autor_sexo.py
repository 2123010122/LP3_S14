# Generated by Django 5.0.6 on 2024-06-29 19:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("miapp", "0003_autor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="autor",
            name="pais",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="autor",
            name="sexo",
            field=models.CharField(max_length=50),
        ),
    ]