# Generated by Django 2.1.5 on 2019-01-20 20:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('careers', '0004_auto_20190120_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActivityRef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField(choices=[(1, '点赞'), (2, '收藏')], verbose_name='操作类型')),
                ('data_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间')),
            ],
        ),
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=models.IntegerField(choices=[(1, '即将开始'), (2, '进行中'), (3, '已结束'), (4, '无状态')], default=4, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='dynamicgroupref',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.Activity', verbose_name='活动'),
        ),
        migrations.AddField(
            model_name='useractivityref',
            name='activity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.Activity', verbose_name='活动'),
        ),
        migrations.AddField(
            model_name='useractivityref',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]