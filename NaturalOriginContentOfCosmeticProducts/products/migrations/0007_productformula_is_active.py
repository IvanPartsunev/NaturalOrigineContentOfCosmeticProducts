# Generated by Django 5.0.2 on 2024-03-31 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_productformula_formula_natural_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productformula',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
