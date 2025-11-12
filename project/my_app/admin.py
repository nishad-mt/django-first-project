from django.contrib import admin
from . models import SignupModel,LibraryModel,BookModel
@admin.register(SignupModel)
class SignupAdmin(admin.ModelAdmin):
    list_display = ['username','email','password']
    
@admin.register(LibraryModel)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ['title','author','price','description','image']
    
@admin.register(BookModel)
class BookAdmin(admin.ModelAdmin):
    list_display =  ['title','author','description','image']
    

    
