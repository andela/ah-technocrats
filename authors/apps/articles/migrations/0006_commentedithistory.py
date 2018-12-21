# Generated by Django 2.1 on 2018-12-21 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20181219_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentEditHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=1000)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='articles.Comment')),
            ],
            options={
                'db_table': 'comment_edits',
            },
        ),
    ]