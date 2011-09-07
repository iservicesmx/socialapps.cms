from django.db import models
from django.db.models.query import QuerySet

class BaseContentQuerySet(QuerySet):
    def active(self):
        """
        Return only "active" (i.e. published) content.
        """
        #TODO: This will be replace by django-workflow
        
        return self.filter(status__exact=self.model.ACTIVE)

class BaseContentManager(models.Manager):
    def get_query_set(self):
        return BaseContentQuerySet(self.model)

    def active(self):
        return self.get_query_set().active()
