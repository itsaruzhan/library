from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Student)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(BookReturnedRecord)
admin.site.register(UserDebt)
admin.site.register(BookRating)
admin.site.register(Login)
admin.site.register(Order)
admin.site.register(OrderItem)


