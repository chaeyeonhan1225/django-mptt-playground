# Generated by Django 5.0.4 on 2024-04-20 05:10

import django.db.models.deletion
from django.db import migrations, models

def create_default_category(apps, schema_editor):
    db = schema_editor.connection.alias
    category = apps.get_model(app_label='category', model_name='Category')

    root = category.objects.using(db).create(name="옷", level=1)
    top = category.objects.using(db).create(name="상의", parent=root, level=2)
    bottom = category.objects.using(db).create(name="하의", parent=root, level=2)
    category.objects.using(db).create(name="원피스", parent=root, level=2)

    category.objects.using(db).create(name="니트", parent=top, level=3)
    category.objects.using(db).create(name="셔츠", parent=top, level=3)

    category.objects.using(db).create(name="바지", parent=bottom, level=3)
    category.objects.using(db).create(name="치마", parent=bottom, level=3)

def reverse_default_category(apps, schema_editor):
    db = schema_editor.connection.alias
    category = apps.get_model(app_label='category', model_name='Category')

    category.objects.using(db).delete()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('level', models.IntegerField(default=1)),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
        migrations.RunPython(create_default_category, reverse_default_category)
    ]
