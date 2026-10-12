from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserForm(UserCreationForm):
    email=forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter The Email'})
    )
    class Meta:
        model=User
        fields=['username','email']

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Enter The UserName'}) 
        self.fields['password1'].widget.attrs.update({'class':'form-control','placeholder':'Enter The Password'}) 
        self.fields['password2'].widget.attrs.update({'class':'form-control','placeholder':'Enter The Re-Password'})    