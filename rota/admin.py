from django.contrib import admin

from .models import Day, Location, Provider, Customer, Driver, RepeatedJourney, SingleJourney, AllocatedJourney, CompletedJourney

class SingleJourneyInline(admin.TabularInline):
  model = SingleJourney

class AllocatedJourneyInline(admin.TabularInline):
  model = AllocatedJourney

class CustomerAdmin(admin.ModelAdmin):
  inlines = [
    SingleJourneyInline
  ]

class DriverAdmin(admin.ModelAdmin):
  inlines = [
    AllocatedJourneyInline
  ]

admin.site.register(Day)
admin.site.register(Location)
admin.site.register(Provider)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(RepeatedJourney)
admin.site.register(SingleJourney)
admin.site.register(AllocatedJourney)
admin.site.register(CompletedJourney)
