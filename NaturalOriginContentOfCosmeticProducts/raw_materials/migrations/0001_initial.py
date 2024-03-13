# Generated by Django 5.0.2 on 2024-03-13 19:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RawMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_name', models.CharField(unique=True)),
                ('inci_name', models.CharField()),
                ('material_type', models.CharField(choices=[('NA', 'Natural'), ('ND', 'Natural derived'), ('NN', 'Non natural')])),
                ('natural_origin_content', models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(50)])),
                ('created_on', models.DateField(auto_now_add=True)),
                ('edited_on', models.DateField(auto_now=True)),
            ],
        ),
    ]
