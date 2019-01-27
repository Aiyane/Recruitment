# Generated by Django 2.1.5 on 2019-01-20 18:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import utils.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classification', models.IntegerField(choices=[(1, '比赛'), (2, '动态'), (3, '实验室介绍'), (4, '招聘信息')], verbose_name='类型')),
                ('status', models.IntegerField(choices=[(1, '即将开始'), (2, '进行中'), (3, '已结束'), (4, '无状态')], default=1, verbose_name='状态')),
                ('text', models.TextField(verbose_name='文本')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='开始时间')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='结束时间')),
                ('likes', models.IntegerField(default=0, verbose_name='点赞数')),
                ('comments', models.IntegerField(default=0, verbose_name='评论数')),
                ('collects', models.IntegerField(default=0, verbose_name='收藏数')),
            ],
            options={
                'verbose_name': '活动',
                'verbose_name_plural': '活动',
                'db_table': 'activity',
            },
        ),
        migrations.CreateModel(
            name='DynamicGroupRef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间')),
                ('dynamic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.Activity', verbose_name='动态')),
            ],
            options={
                'db_table': 'activity_group_ref',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('superior', models.IntegerField(default=0, verbose_name='上级id')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='名字')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '职业圈',
                'verbose_name_plural': '职业圈',
                'db_table': 'group',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(storage=utils.storage.ImageStorage(), upload_to='dynamic/%Y/%m', verbose_name='图片')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间')),
                ('dynamic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.Activity', verbose_name='动态')),
            ],
            options={
                'verbose_name': '图片',
                'verbose_name_plural': '图片',
                'db_table': 'image',
            },
        ),
        migrations.AddField(
            model_name='dynamicgroupref',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='careers.Group', verbose_name='职业圈'),
        ),
    ]