from django.db import models
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
import uuid

class Test_Table_One(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=10, null=False)
    description = models.TextField()
    value = models.IntegerField(null=False)
    state = models.BooleanField(null=False)
    datetime_register = models.DateTimeField(default=timezone.now)
    tabletwo = models.ManyToManyField('enerbit.Test_Table_Two', through='Test_Manytomany')

class Test_Table_Two(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=10, null=False)
    description = models.TextField()
    value = models.IntegerField(null=False)
    state = models.BooleanField(null=False)
    datetime_register = models.DateTimeField(default=timezone.now)
    tableone = models.ManyToManyField('enerbit.Test_Table_One', through='Test_Manytomany')

class Test_Onetomany(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=10, null=False)
    description = models.TextField()
    value = models.IntegerField(null=False)
    state = models.BooleanField(null=False)
    datetime_register = models.DateTimeField(default=timezone.now)
    test_table_one = models.ForeignKey('enerbit.Test_Table_One', on_delete=models.CASCADE)

class Test_Manytomany(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    test_table_one = models.ForeignKey('enerbit.Test_Table_One', on_delete=models.CASCADE)
    test_table_two = models.ForeignKey('enerbit.Test_Table_Two', on_delete=models.CASCADE)
    datetime_register = models.DateTimeField(default=timezone.now)