import imp
from django.shortcuts import render, redirect
from .forms import NewStudentForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login,  authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db import connection
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    return render(request, 'library/home.html')

@login_required(login_url='login')
def categories(request):
    cats = Category.objects.all()
    return render(request, 'library/categories.html', {'cats':cats})

@login_required(login_url='login')
def showBooks(request):
    return render(request, 'library/showBooks.html')


def register_request_student(request):
    if request.method == 'POST':
       
        form = NewStudentForm(request.POST)
        print(request.POST)
        if form.is_valid():
            print('valid')
            
            user = form.save()
            user.refresh_from_db()  
            user.student.fname = form.cleaned_data.get('first_name')
            user.student.lname = form.cleaned_data.get('last_name')
            user.student.email = form.cleaned_data.get('email')
            user.student.course = form.cleaned_data.get('course')
            user.student.gender = form.cleaned_data.get('gender')
            user.student.faculty = form.cleaned_data.get('faculty')
            user.student.save
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')

    else:
        form = NewStudentForm()
    print('invalid')
    return render(request, 'library/registration_student.html', {'register_form': form})

def login_request(request):
  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      cursor = connection.cursor()
    
      cursor.execute( "declare a_date DATE := trunc(SYSDATE); begin insert into library_login(action,action_date, user_id) values(1, a_date, %d ); end; " %
    ( user.id))          
      if user is not None:
        login(request, user)
        messages.info(request, f"You are now logged in as {username}.")
        return redirect("profile", id = user.id) 
      else:
        messages.error(request,"Invalid username or password.")
    else:
      messages.error(request,"Invalid username or password.")
  form = AuthenticationForm()
  return render(request=request, template_name="library/login.html", context={"login_form":form})


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def mainpage_books(request):
    newBooks1=Book.objects.filter().order_by('-book_id')[:4]
    newBooks2=Book.objects.filter().order_by('-book_id')[4:8]
    newBooks3=Book.objects.filter().order_by('-book_id')[8:12]
    topBooks1=Book.objects.filter().order_by('average_rating')[:4]
    topBooks2=Book.objects.filter().order_by('average_rating')[4:8]
    topBooks3=Book.objects.filter().order_by('average_rating')[8:12]
    return render(request, 'library/main.html', {'newBooks1': newBooks1,'newBooks2': newBooks2, 'newBooks3': newBooks3,'topBooks1':topBooks1, 'topBooks2':topBooks2, 'topBooks3':topBooks3})

def bookByCategory(request, category_slug):
    cat =get_object_or_404(Category, slug=category_slug)
    books = Book.objects.filter(category_id=cat.category_id)
    content = {'books':books}
    return render(request, 'library/bookByCategory.html',content)

@login_required(login_url='login')
def textbooks(request):
    textBooks = Book.objects.filter(category_id=1)
    return render(request, 'library/textBooks.html', {'textBooks':textBooks })

@login_required(login_url='login')
def dramaBooks(request):
    dramaBooks = Book.objects.filter(category_id=3)
    return render(request, 'library/drama.html', {'dramaBooks': dramaBooks})

@login_required(login_url='login')
def scienceBooks(request):
    scienceBooks = Book.objects.filter(category_id=2)
    return render(request, 'library/science.html', {'scienceBooks': scienceBooks})

@login_required(login_url='login')
def biographyBooks(request):
    biographyBooks = Book.objects.filter(category_id=4)
    return render(request, 'library/biography.html', {'biographyBooks': biographyBooks})

@login_required(login_url='login')
def my_profile(request, id):
    student = User.objects.get(id=id)
    return render(request, 'library/profile.html',  context={"user":student})


class DetailCart(DetailView):
    model = Cart
    template_name='cart/detail_cart.html'

class ListCart(ListView):
    model = Cart
    context_object_name = 'carts'
    template_name='cart/list_carts.html'

class CreateCart(CreateView):
    model = Cart
    template_name = 'cart/create_cart.html'

class Updatecart(UpdateView):
    model = Cart
    template_name = 'cart/update_cart.html'

class DeleteCart(DeleteView):
    model = Cart
    template_name = 'cart/delete_cart.html'  

class DetailCartItem(DetailView):
    model = CartItem
    template_name='cartitem/detail_cartitem.html'

class ListCartItem(ListView):
    model = CartItem
    context_object_name = 'cartitems'
    template_name='library/list_cartitems.html'

class CreateCartItem(CreateView):
    model = CartItem
    template_name = 'cartitem/create_cartitem.html'

class UpdateCartItem(UpdateView):
    model = CartItem
    template_name = 'cartitem/update_cartitem.html'

class DeleteCartItem(DeleteView):
    model = Cart
    template_name = 'cartitem/delete_cartitem.html'

    