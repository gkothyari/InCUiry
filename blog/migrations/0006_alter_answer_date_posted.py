# Generated by Django 3.2 on 2021-04-28 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_rename_qid_answer_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='date_posted',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
