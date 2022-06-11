# Generated by Django 4.0.4 on 2022-05-17 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_alter_order_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.PositiveSmallIntegerField(choices=[(0, 'карта'), (1, 'наличные')], db_index=True),
        ),
    ]
