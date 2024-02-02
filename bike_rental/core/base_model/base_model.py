from django.db import models
from django.db.models import Manager, QuerySet


class AppManager(Manager):
    def get_queryset(self):
        """
        Returns a QuerySet excluding records with 'is_deleted' set to True.
        """
        return QuerySet(self.model, using=self._db).exclude(is_deleted=True)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    is_deleted = models.BooleanField(default=False)
    objects = AppManager()

    def delete(self):
        """Mark the record as deleted instead of deleting it"""

        self.is_deleted = True
        self.save()

