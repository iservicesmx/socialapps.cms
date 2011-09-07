from django.db import models
from django.db.models.query import QuerySet
from django.http import Http404

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

    def get_object(self, path, active=True,raise404=False):
        if path.endswith('/'):
            path = path[:-1]
        slug = path.split("/")[-1]
        
        try:
            if active:
                return self.active().get(slug=slug)
            else:
                return self.get(slug=slug)
        except self.model.DoesNotExist:
            if raise404:
                raise Http404
            raise
        