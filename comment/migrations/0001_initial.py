# Generated by Django 2.2.13 on 2020-09-16 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('text', models.TextField()),
                ('comment_time', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_comment', to='comment.Comment')),
                ('reply_to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_user', to=settings.AUTH_USER_MODEL)),
                ('root', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leaf_comment', to='comment.Comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['comment_time'],
            },
        ),
    ]
