import cx_Oracle
from django.shortcuts import render, redirect
from .forms import NewStudentForm
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login,  authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, View
from .models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone

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
      cursor.callproc("user_action", [user.id])
      cursor.close()
      
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

@login_required(login_url='login')
def bookByCategory(request, category_slug):
    cat =get_object_or_404(Category, slug=category_slug)
    books = Book.objects.filter(category_id=cat.category_id)
    content = {'books':books, 'cat': cat}
    return render(request, 'library/booksByCat.html',content)

@login_required(login_url='login')
def viewBook(request, book_slug):
    book = Book.objects.get(slug = book_slug)
    content = {'book':book}
    return render(request, 'library/book.html',content)

@login_required(login_url='login')
def my_profile(request, id):
    student = User.objects.get(id=id)
    cursor = connection.cursor()
    startYear =  cursor.callfunc('calculate_year',cx_Oracle.NUMBER , [student.student.stud_id])
    debt =  cursor.callfunc('show_debt',cx_Oracle.NUMBER , [student.id])
    startYear = int(startYear)
    debt = int(debt)
    return render(request, 'library/profile.html',  context={"user":student, "startYear":startYear, "debt": debt })


@login_required
def add_to_cart(request, book_slug):
    item = get_object_or_404(Book, slug=book_slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'library/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("home")
