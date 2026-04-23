import django.db.models.deletion
import myauth.models
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ("myauth", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile",
            options={"verbose_name": "Profile", "verbose_name_plural": "Profiles"},
        ),
        migrations.RemoveField(
            model_name="profile",
            name="agreement_accepted",
        ),
        migrations.AddField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=myauth.models.user_avatar_path,
                verbose_name="Avatar",
            ),
        ),
        migrations.AddField(
            model_name="profile",
            name="birth_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="phone_number",
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AlterField(
            model_name="profile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
