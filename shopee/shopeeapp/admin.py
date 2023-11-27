from django.contrib import admin
from shopeeapp.models import Index

class IndexAdmin(admin.ModelAdmin):
    list_display=['id','cat','bname','mname','price','oprice','offer','ss','hds','os','rms','is_active']
    list_filter=['cat','is_active']

admin.site.register(Index,IndexAdmin)
