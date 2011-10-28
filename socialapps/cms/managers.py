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

    def get_base_object(self, path, active=True,raise404=True):
        if path.endswith('/'):
            path = path[:-1]
        paths = path.split("/")
        
        try:
            obj = self.get(slug=paths[0], parent=None)
        except self.model.DoesNotExist:
            raise Http404
            
        for path in paths[1:]:
            try:
                obj = obj.get_children().get(slug=path)
            except self.model.DoesNotExist:
                raise Http404
                
        return obj
                
