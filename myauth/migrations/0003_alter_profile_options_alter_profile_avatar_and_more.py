import myauth.models
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("myauth", "0002_alter_profile_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile",
            options={"verbose_name": "Профиль", "verbose_name_plural": "Профили"},
        ),
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=myauth.models.user_avatar_path,
                verbose_name="Аватар",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=models.TextField(blank=True, max_length=500, verbose_name="О себе"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="birth_date",
            field=models.DateField(blank=True, null=True, verbose_name="Дата рождения"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="phone_number",
            field=models.CharField(blank=True, max_length=15, verbose_name="Телефон"),
        ),
    ]
