# Generated by Django 2.2.5 on 2021-01-15 14:36

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Spit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=40)),
                ('publishtime', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('visits', models.IntegerField()),
                ('thumbup', models.IntegerField()),
                ('comment', models.IntegerField()),
                ('collected', models.BooleanField(default=False)),
                ('hasthumbup', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spit.Spit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '吐槽',
                'verbose_name_plural': '吐槽',
                'db_table': 'tb_spit',
            },
        ),
    ]
