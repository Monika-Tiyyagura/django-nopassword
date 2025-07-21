# nopassword/migrations/0004_enable_pgcrypto.py

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('nopassword', '0003_alter_logincode_expires_at'),
    ]

    operations = [
        migrations.RunSQL('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
    ]
