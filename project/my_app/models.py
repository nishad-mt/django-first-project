from django.db import models

class SignupModel(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)  # store hashed password
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
class LibraryModel(models.Model):
    title = models.CharField()
    author = models.CharField()
    description = models.TextField()
    image = models.ImageField()
    price = models.IntegerField()
    
class BookModel(models.Model):
    title = models.CharField()
    author = models.CharField()
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    lib_user = models.ForeignKey(SignupModel,on_delete=models.CASCADE,null=True, blank=True)



    
