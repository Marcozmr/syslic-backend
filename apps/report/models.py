from django.db import models

class Report(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            blank=False,
                            null=False)

    module = models.CharField(max_length=100,
                              unique=True,
                              blank=False,
                              null=False)

    superset_id = models.CharField(max_length=100,
                                   unique=True,
                                   blank=False,
                                   null=False)

    default = models.BooleanField(default=False)
