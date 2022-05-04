from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Student)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(BookReturnedRecord)
admin.site.register(UserDebt)
admin.site.register(BookRating)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Login)
class CartAdmin(admin.ModelAdmin):
    pass

class CartItemAdmin(admin.ModelAdmin):
    pass