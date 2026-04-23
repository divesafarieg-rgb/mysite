import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Имя автора")),
                ("bio", models.TextField(blank=True, verbose_name="Биография")),
            ],
            options={
                "verbose_name": "Автор",
                "verbose_name_plural": "Авторы",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=40, verbose_name="Название категории"),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20, verbose_name="Название тега")),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Заголовок")),
                ("content", models.TextField(verbose_name="Содержимое")),
                (
                    "pub_date",
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name="Дата публикации",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="articles",
                        to="blogapp.author",
                        verbose_name="Автор",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="articles",
                        to="blogapp.category",
                        verbose_name="Категория",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        blank=True,
                        related_name="articles",
                        to="blogapp.tag",
                        verbose_name="Теги",
                    ),
                ),
            ],
            options={
                "verbose_name": "Статья",
                "verbose_name_plural": "Статьи",
                "ordering": ["-pub_date"],
            },
        ),
    ]
