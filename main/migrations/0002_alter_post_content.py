# Generated by Django 4.1.2 on 2022-10-25 11:07

from django.db import migrations
import django_editorjs_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_editorjs_fields.fields.EditorJsJSONField(blank=True, default='Контент', null=True),
        ),
    ]