# Generated by Django 5.0.2 on 2024-03-21 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculate_noi', '0007_alter_productformula_product'),
        ('raw_materials', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productformularawmaterial',
            name='raw_material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='raw_materials', to='raw_materials.rawmaterial'),
        ),
    ]
