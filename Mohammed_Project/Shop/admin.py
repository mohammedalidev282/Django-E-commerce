from django.contrib import admin 
from .models import *

"""class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','image','description','status')
 """   



# Register your models here.
admin.site.register(Category)
admin.site.register(Product)

