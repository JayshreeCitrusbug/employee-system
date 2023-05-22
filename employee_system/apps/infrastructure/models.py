# python imports
import string
from dataclasses import dataclass
from datetime import datetime

# django imports
from django.contrib import admin
from django.db import models


# class Manager(models.Manager):
#     def dfilter(self, *args, **kwargs):
#         return self.filter(is_deleted=False, **kwargs)
    
class ActivityModel(models.Model):
    """
    A Activity model which includes fields that reflect when the model has been created
    or modified, and active status
    """

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    # is_deleted = models.BooleanField(default=False, db_index=True)

    # objects = Manager()

    # def delete(self):
    #     self.is_deleted = True
    #     self.save(update_fields=["is_deleted"])

    class Meta:
        abstract = True


   
@dataclass(frozen=True)
class ActivityModelData:
    created_at: datetime
    modified_at: datetime
    is_active: bool


# class WithOutDeletedModelsManager(models.Manager):
#     """
#     This requires that the model using this manager has an is_deleted boolean attribute
#     """
#     def get_queryset(self):
#         return super().get_queryset().filter(is_deleted=False)


# class AdminWithAllDeletedModels(admin.ModelAdmin):
#     def get_queryset(self, request):
#         """
#         Override queryset to use the base manager that returns all rows including the deleted ones
#         """
#         qs = self.model._base_manager.get_queryset()
#         ordering = self.get_ordering(request)
#         if ordering:
#             qs = qs.order_by(*ordering)
#         return qs
