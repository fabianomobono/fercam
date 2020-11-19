from django.contrib import admin
from .models import  Trip, User, Order, Driver_pay, Size_coefficient, Time_coefficient, Weight_coefficient, Distance_coefficient, Cargo_picture, Message
import admin_thumbnails

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['id']


# Register your models here.
class Cargo_pictureAdmin(admin.ModelAdmin):
    fields = ['image_tag']
    readonly_fields = ['image_tag']

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'time_order_was_placed')


admin.site.register(Message)
admin.site.register(Cargo_picture)
admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Trip)
admin.site.register(Driver_pay)
admin.site.register(Size_coefficient)
admin.site.register(Time_coefficient)
admin.site.register(Weight_coefficient)
admin.site.register(Distance_coefficient)
