from django.shortcuts import render,redirect
from . forms import SignUpForm,LoginForm,BooksForm,EditProfileForm
from . models import SignupModel,LibraryModel,BookModel
from django.views.decorators.cache import never_cache
from django.contrib import messages

@never_cache
def Signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request,"signup.html",{'form':form})

@never_cache
def login(request):
    if request.session.get('email'):
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            if SignupModel.objects.filter(email=email, password=password).exists():
                user = SignupModel.objects.get(email=email)
                request.session['email'] = user.email
                request.session['id'] = user.id
                return redirect('home')
            else:
                # Clear old messages before adding a new one
                storage = messages.get_messages(request)
                storage.used = True  #Marks any old messages as used,
                #so they won’t be displayed again.
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Please correct the form errors.") 
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@never_cache
def home(request):
    if not request.session.get('email'):
        return redirect('login')
    return render(request,"home.html")

@never_cache
def library(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')
    books = LibraryModel.objects.all()
    return render(request,"library.html",{'books':books})

@never_cache  
def create(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')
    user = SignupModel.objects.get(id=user_id)
        
    if request.method == 'POST':
        form = BooksForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.lib_user = user    
            instance.save()
            return redirect('view')
        else:
            return render(request,"create.html",{'form':form})
    else:
        form = BooksForm()
    return render(request,"create.html",{'form':form})

@never_cache
def list_view(request):
    user_email = request.session.get('email')
    if user_email:
        user = SignupModel.objects.get(email=user_email)
        books = BookModel.objects.filter(lib_user=user)
        return render(request,'read.html',{'books':books}) 
    else:
        return render(request,'login.html') 
        
@never_cache    
def edit(request, id):
    u_email = request.session.get('email')
    if not u_email:
        return redirect('login')  # safety check if session expired

    user = SignupModel.objects.get(email=u_email)

    try:
        book = BookModel.objects.get(id=id, lib_user=user)
    except BookModel.DoesNotExist:
        return redirect('view')  # redirect if no such book exists for this user

    if request.method == "POST":
        form = BooksForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            buk_obj = form.save(commit=False)
            buk_obj.lib_user = user  # ensure book stays linked to user
            buk_obj.save()
            return redirect('view')
    else:
        form = BooksForm(instance=book)

    return render(request, "edit.html", {'form': form, 'book': book})

@never_cache
def delete(request,id):
    user_email = request.session.get('email')
    if user_email:
        book = BookModel.objects.get(id=id)
        book.delete()
        return redirect('view')
    return redirect('login')

@never_cache
def profile(request):
    user_email = request.session.get('email')
    if not user_email:
        return redirect('login')
    user = SignupModel.objects.get(email=user_email)
    return render(request, 'profile.html', {'user': user})
@never_cache
def edit_profile(request):
    user_id = request.session.get('id')
    if not user_id:
        return redirect('login')
    
    user = SignupModel.objects.get(id=user_id)

    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user)
    
    return render(request, "edit_profile.html", {'form': form})

def logout(request):
    request.session.flush()
    return redirect('login')
    