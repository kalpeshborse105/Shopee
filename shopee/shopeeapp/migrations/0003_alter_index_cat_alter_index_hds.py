# Generated by Django 4.2.3 on 2023-07-16 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopeeapp', '0002_customer_alter_cart_pid_alter_cart_userid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='index',
            name='cat',
            field=models.IntegerField(choices=[(1, 'Acer'), (4, 'HP'), (3, 'Dell'), (5, 'Lenovo'), (2, 'Asus')], verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='index',
            name='hds',
            field=models.CharField(max_length=30, verbose_name='Hard Disk Size'),
        ),
    ]