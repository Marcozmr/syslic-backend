from django.db import models

class OrderAuditPercentageManager(models.Manager):
    def instance(self):
        return self.get(pk=1)
