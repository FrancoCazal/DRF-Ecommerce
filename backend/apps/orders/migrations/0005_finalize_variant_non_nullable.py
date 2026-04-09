# Migration 3/3: Make variant non-nullable and remove product FK from OrderItem.
# Safe to apply because migration 0004 already populated variant for all existing rows.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_populate_variant_from_product'),
        ('products', '0002_remove_product_image_remove_product_price_and_more'),
    ]

    operations = [
        # Remove the old product FK
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        # Make variant non-nullable
        migrations.AlterField(
            model_name='orderitem',
            name='variant',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='order_items',
                to='products.productvariant',
            ),
        ),
    ]
