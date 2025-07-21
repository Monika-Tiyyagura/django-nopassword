#0004_logincode_add_uuid_field.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('nopassword', '0003_alter_logincode_expires_at'),
    ]

    operations = [
        # Step 1: Add a new UUID field (nullable for now)
        migrations.AddField(
            model_name='logincode',
            name='uuid',
            field=models.UUIDField(null=True, blank=True),
        ),
    ]
