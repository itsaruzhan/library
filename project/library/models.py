from tabnanny import verbose
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.template.defaultfilters import slugify


# Create your models here.


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER = [
        ('M',  'Male') , 
        ('F',  'Female')
    ]
    FACULTY = [
        ('EDU', 'Education'),
        ('ENG', 'Engineering and Natural Sciences'),
        ('BS', 'Business School'),
        ('L', 'Law')
    ]
    stud_id = models.BigAutoField(primary_key=True)
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    email = models.EmailField()
    course = models.IntegerField(default=1)
    gender = models.CharField(choices=GENDER, default='None', max_length=10)
    faculty = models.CharField(choices = FACULTY, default='None', max_length=50)
    
    
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Student.objects.create(user=instance)
    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.student.save()
        
    def __str__(self):
        return self.user.username
    
class Category(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image =  models.ImageField(upload_to='img', blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)    
    
class Book(models.Model):
    book_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=False, null=False)
    image = models.ImageField(upload_to='img', blank=True, null=True)
    edition = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=100, blank=False, null=False)
    publisher = models.CharField(max_length=100)
    copies = models.IntegerField()
    available = models.BooleanField()
    average_rating = models.DecimalField(decimal_places=1, max_digits = 2)
    category_id = models.ForeignKey(Category, related_name='books', on_delete=models.DO_NOTHING)
    description = models.TextField()
    
    def __str__(self):
        return self.title
    
 
class BookReturnedRecord(models.Model):
    borrower_id =  models.BigAutoField(primary_key=True)
    book_id = models.ForeignKey(Book, on_delete=models.DO_NOTHING)   
    stud_id = models.ForeignKey(Student, related_name='borrows', on_delete=models.DO_NOTHING)
    taken_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    returned = models.BooleanField()
        

class UserDebt(models.Model):
    debt_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=3,decimal_places=2)
    days = models.IntegerField()
    book_info = models.ForeignKey(BookReturnedRecord, on_delete=models.DO_NOTHING)
    paid = models.BooleanField() 
    
class BookRating(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    
   
    
class Login(models.Model):
    user_id = models.IntegerField()
    action = models.BooleanField()   
    action_date = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)    