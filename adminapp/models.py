from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager 
# Create your models here.

class UserManager(BaseUserManager): 
    def create_user(self, email, password=None): 
        if not email: 
            raise ValueError("Users must have an email address") 
        email = self.normalize_email(email) 
        user = self.model(email=email) 
        user.set_password(password) 
        user.save(using=self._db) 
        return user 
        
        
    def create_superuser(self, email, password): 
             user = self.create_user(email, password) 
             user.is_admin = True 
             User.is_superuser = True 
             user.save(using=self._db) 
             return user 
        
class User(AbstractBaseUser): 
    email = models.EmailField(unique=True) 
    name = models.CharField(max_length =255) 
    is_active = models.BooleanField(default=True) 
    is_admin = models.BooleanField(default=False) 
    objects = UserManager() 
 
    USERNAME_FIELD = 'email'

    
class Recipe(models.Model):

    Difficulty_level = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    views = models.IntegerField(default=0)
    image = models.FileField()
    difficulty_level = models.CharField(max_length=10, choices=Difficulty_level, default='Easy')
    Cooking_time = models.IntegerField(default=0)
    Createdby = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)

    


    
    




       
    

