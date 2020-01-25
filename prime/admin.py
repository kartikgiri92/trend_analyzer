from django.contrib import admin
import prime.models as prime_models

# Register your models here.
admin.site.register(prime_models.Trend)
admin.site.register(prime_models.Tweet)
admin.site.register(prime_models.Log)