# Generated by Django 5.0.2 on 2024-03-21 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productformula_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productformularawmaterial',
            name='raw_material_content',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
