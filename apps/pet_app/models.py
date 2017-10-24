# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..logreg_app.models import User

class PetManager(models.Manager):
    def pet_validator(self, postData):
        errors = {}
        if len(postData['name']) == 0:
            errors["all_fields_required"] = "All fields are required"
        if len(postData['name']) < 2:
            errors['name'] = "First name must be least 2 characters long"
        if not postData['name'].isalpha():
            errors['name_is_valid'] = "First name can only contain letters"
        return errors
# Create your models here.
class Kind(models.Model):
    name = models.CharField(max_length=50)

class Pet(models.Model):
    name =  models.CharField(max_length=50)
    kind = models.ForeignKey(Kind, related_name="pets")
    user = models.ForeignKey(User, related_name="pets")
    objects = PetManager()