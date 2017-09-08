from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Day(models.Model):
  name                    = models.CharField(max_length=10)
  description             = models.CharField(max_length=300, blank=True)

  def __str__(self):
    return self.name

class Location(models.Model):
  name                    = models.CharField(max_length=100, blank=True)
  address                 = models.CharField(max_length=100)

  def __str__(self):
    if not self.name:
      return self.address
    else:
      return self.name

class Provider(models.Model):
  name                    = models.CharField(max_length=50)

  def __str__(self):
    return self.name

class Customer(models.Model):
  first_name              = models.CharField(max_length=30)
  last_name               = models.CharField(max_length=30)
  address                 = models.ForeignKey(
                              Location,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True
                            )
  provider                = models.ForeignKey(
                              Provider,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True
                            )

  def __str__(self):
    return self.first_name + ' ' + self.last_name

class Driver(models.Model):
  first_name              = models.CharField(max_length=30)
  last_name               = models.CharField(max_length=30)

  def __str__(self):
    return self.first_name + ' ' + self.last_name

class RepeatedJourney(models.Model):
  customer                = models.ForeignKey(
                              Customer,
                              on_delete=models.CASCADE
                            )
  pickup_time             = models.TimeField()
  return_time             = models.TimeField(blank=True, null=True)
  origin                  = models.ForeignKey(
                              Location,
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='repeated_journeys_from'
                            )
  destination             = models.ForeignKey(
                              Location,
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='repeated_journeys_to'
                            )
  price                   = models.DecimalField(decimal_places=2, max_digits=10)
  days                    = models.ManyToManyField(Day)

  def __str__(self):
    return self.destination.name
  
class SingleJourney(models.Model):
  customer                = models.ForeignKey(
                              Customer,
                              on_delete=models.CASCADE
                            )
  pickup_time             = models.TimeField()
  return_time             = models.TimeField(blank=True, null=True)
  origin                  = models.ForeignKey(
                              Location,
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='single_journeys_from'
                            )
  destination             = models.ForeignKey(
                              Location,
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='single_journeys_to'
                            )
  price                   = models.DecimalField(decimal_places=2, max_digits=10)

  def __str__(self):
    return self.destination.name

class AllocatedJourney(models.Model):
  journey_type            = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  journey_object_id       = models.PositiveIntegerField()
  journey                 = GenericForeignKey('journey_type', 'journey_object_id')              
  date                    = models.DateField()
  driver                  = models.ForeignKey(
                            Driver,
                            on_delete=models.CASCADE,
                            blank=True,
                            null=True
                            )

  def __str__(self):
    return 'Allocated Journey'

class CompletedJourney(models.Model):
  allocated_journey       = models.ForeignKey(
                              AllocatedJourney,
                              on_delete=models.CASCADE
                            )
  COMPLETED = 0;CANCELLED = 1;NO_SHOW = 2;DRIVER_NO_SHOW = 3
  OUTCOME_CHOICES         = (
    (COMPLETED,      'Completed'),
    (CANCELLED,      'Cancelled'), 
    (NO_SHOW,        'No show'),
    (DRIVER_NO_SHOW, 'Driver no show')
  )
  outcome                 = models.PositiveSmallIntegerField(choices=OUTCOME_CHOICES)
  replacement_destination = models.ForeignKey(
                              Location,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True
                            )
  replacement_driver      = models.ForeignKey(
                              Driver,
                              on_delete=models.SET_NULL,
                              blank=True,
                              null=True
                            )
  replacement_price       = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)

  def __str__(self):
    return self.allocated_journey.name
