from django import forms
from . models import SignupModel,BookModel

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignupModel
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')  
        
        if password and len(password) < 8:
            raise forms.ValidationError("Password must have atleast 8 characters")      

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password do not match")
    
        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username','').strip()
        if not username.replace(" ", "").isalpha():
            raise forms.ValidationError("Name must contain only letters")

        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Email must end with @gmail.com")
        if SignupModel.objects.filter(email=email).exists():
            raise forms.ValidationError("This Email is already registered")
        
        return email
class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class BooksForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields = '__all__'
        exclude = ['lib_user',]
        
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = SignupModel
        fields = ['username', 'email',]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id
        if SignupModel.objects.filter(email=email).exclude(id=user_id).exists():
            raise forms.ValidationError("This email is already in use by another account.")
        return email
             
       
            
    

            
