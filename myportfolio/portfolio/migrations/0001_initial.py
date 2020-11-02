# Generated by Django 2.2.11 on 2020-11-02 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proj_name', models.CharField(max_length=200)),
                ('category', models.CharField(default='', max_length=50)),
                ('proj_desc', models.CharField(max_length=300)),
                ('proj_image', models.ImageField(default='', upload_to='')),
                ('proj_file', models.FileField(default=None, upload_to='pf/images')),
                ('pub_date', models.DateField(default=None, max_length=200)),
                ('proj_link1', models.URLField(default=None)),
                ('proj_link2', models.URLField(default=None)),
            ],
        ),
    ]
