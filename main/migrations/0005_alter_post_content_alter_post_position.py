# Generated by Django 4.1.2 on 2022-10-25 11:50

from django.db import migrations, models
import django.db.models.deletion
import django_editorjs_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_editorjs_fields.fields.EditorJsJSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='position',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.release'),
        ),
    ]
