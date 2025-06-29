from django.contrib import admin
from .models import *
from django.utils.html import mark_safe 

class productAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'uuid', 'ProductImage')
    search_fields = ('title',)
    list_filter = ('title', 'category', 'price')
    readonly_fields = ('ProductImage1','ProductImage2','ProductImage3')
    
    
class contactAdmin(admin.ModelAdmin):
    list_display = ('name','phone','message')
    
class categoryAdmin(admin.ModelAdmin):
    list_display = ('name','img')
    readonly_fields = ('img',)
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_email')

admin.site.register(Category, categoryAdmin)
admin.site.register(Product, productAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Contact, contactAdmin)
admin.site.register(UserPost,UserAdmin)
