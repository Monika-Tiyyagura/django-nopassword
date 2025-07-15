from django.db import migrations, models
import uuid

class Migration(migrations.Migration):

    dependencies = [
        ('nopassword', '0003_alter_logincode_expires_at'),
    ]

    operations = [
        # Step 1: Add a new UUID field (temporary)
        migrations.AddField(
            model_name='logincode',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]
