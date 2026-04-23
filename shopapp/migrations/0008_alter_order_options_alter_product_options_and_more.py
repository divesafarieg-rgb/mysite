import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("shopapp", "0007_alter_product_options"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="order",
            options={"verbose_name": "order", "verbose_name_plural": "orders"},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={
                "ordering": ["name", "price"],
                "permissions": [
                    ("can_create_product", "Can create product"),
                    ("can_edit_product", "Can edit product"),
                ],
                "verbose_name": "product",
                "verbose_name_plural": "products",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="products",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="created at"),
        ),
        migrations.AlterField(
            model_name="order",
            name="delivery_address",
            field=models.TextField(
                blank=True, null=True, verbose_name="delivery address"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="products",
            field=models.ManyToManyField(
                related_name="orders", to="shopapp.product", verbose_name="products"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="promocode",
            field=models.CharField(blank=True, max_length=20, verbose_name="promocode"),
        ),
        migrations.AlterField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="archived",
            field=models.BooleanField(default=False, verbose_name="archived"),
        ),
        migrations.AlterField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="created at"),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True, verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="product",
            name="discount",
            field=models.SmallIntegerField(default=0, verbose_name="discount"),
        ),
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(max_length=100, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=8, verbose_name="price"
            ),
        ),
    ]
