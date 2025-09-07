# -*- coding: utf-8 -*-
import uuid
import random

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Named function instead of lambda (Django can serialize this)
def default_expiry():
    dt = timezone.now() + timezone.timedelta(hours=24)
    if timezone.is_naive(dt):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
    return dt

class LoginCode(models.Model):
    CODE_LENGTH = 6

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='login_codes',
        editable=False,
        verbose_name=_('user'),
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(editable=False)
    next = models.TextField(editable=False, blank=True)
    expires_at = models.DateTimeField(default=default_expiry, null=True, editable=False)
    code = models.CharField(max_length=6, editable=False)  # Changed max_length to 6

    def __str__(self):
        return "%s - %s" % (self.user, self.timestamp)

    def _generate_code(self):
        """Generate a 6-digit numeric login code."""
        return str(random.randint(100000, 999999))

    def save(self, *args, **kwargs):
        self.timestamp = timezone.now()
        if not self.id:
            self.id = uuid.uuid4()
        if not self.next:
            self.next = '/'
        if not self.code:
        # Generate and assign a 6-digit code before saving
            self.code = self._generate_code()
        super(LoginCode, self).save(*args, **kwargs)

    @classmethod
    def create_code_for_user(cls, user, next=None):
        if not user.is_active:
            return None
        
        #clean up old codes
        cutoff = timezone.now() - timezone.timedelta(hours=720)
        cls.objects.filter(timestamp__lt=cutoff).delete()

        #generate a unique code
        while True:
            code = str(random.randint(10**(cls.CODE_LENGTH-1), 10**cls.CODE_LENGTH - 1))
            if not cls.objects.filter(code=code).exists(): #this checks if code already exists or not
                break

        #create new code
        login_code = LoginCode(user=user, code=code)
        if next is not None:
            login_code.next = next
        login_code.save()
        return login_code
