# Generated by Django 3.2 on 2021-04-27 09:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_answer_posted_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='qid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='blog.post'),
        ),
    ]
