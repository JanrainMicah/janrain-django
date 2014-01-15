from django.conf import settings
from django.db import models

"""
Capture User

Stores the relationship between a Django user and a Capture record.
"""
class CaptureUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    uuid = models.CharField(max_length=38, db_index=True, unique=True,
                            editable=False)

import signals
