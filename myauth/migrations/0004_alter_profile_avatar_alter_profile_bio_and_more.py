import myauth.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myauth", "0003_alter_profile_options_alter_profile_avatar_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=myauth.models.user_avatar_path,
                verbose_name="Avatar",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=models.TextField(blank=True, max_length=500, verbose_name="Bio"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="birth_date",
            field=models.DateField(blank=True, null=True, verbose_name="Birth date"),
        ),
        migrations.AlterField(
            model_name="profile",
            name="phone_number",
            field=models.CharField(
                blank=True, max_length=15, verbose_name="Phone number"
            ),
        ),
    ]
