from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# Create your models here.

class Badge(models.Model):
    """Model representing a badge which congrats a user or model
    """
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    # image = models.ImageField...

    # user = models.ForeignKey(User, related_name="badges", null=True)
    # a Badge can be given to a user or a model or even more.
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')


class Creator3d(models.Model):
    """Model representing a 3D model maker (can upload a model on SketchFab for
    example). A OneToOneField to auth django app link this model as adviced in
    the django doc (
    https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#extending-the-existing-user-model)

    """
    user = models.OneToOneField(User)
    date_creation_sign_in = models.DateField(auto_now_add=True)
    badges = GenericRelation(Badge, related_query_name="users")


class Model3d(models.Model):
    """Model representing a 3D model
    """

    name = models.CharField(null=True, max_length=150)
    description = models.CharField(blank=True, null=True, max_length=500)
    number_of_views = models.IntegerField(blank=True, null=True, default=0)
    creator = models.ForeignKey(Creator3d, related_name='models', null=True)
    # vertices_number = models.IntegerField(null=True, blank=True)
    # file = models.FileField...

    badges = GenericRelation(Badge, related_query_name="models")
