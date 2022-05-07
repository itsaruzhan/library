from unicodedata import name
from django.contrib import admin
from django.urls import path
from django.urls import re_path as url
from . import views
from .views import OrderSummaryView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('home/', views.mainpage_books, name='home'),
    path('register/', views.register_request_student, name='register'),
    path('categories/' , views.categories, name='categories'),
    path('category/<slug:category_slug>', views.bookByCategory, name='bookByCategory'),
    path('books/<int:id>', views.viewBook, name = 'viewBook'),
    path('login/' , views.login_request, name='login'),
    path('logout/', views.logoutUser, name="logout"),
    path('showBooks/', views.showBooks, name="showBooks"),
    path('profile/<int:id>', views.my_profile, name='profile'),
    path('book/<slug:book_slug>/',views.viewBook, name='book'),
    path('add-to-cart/<slug>/',views.add_to_cart, name='add-to-cart'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)