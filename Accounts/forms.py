from re import A
from django import forms
from .models import Account,UserProfile

class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password','class':'form-control'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'form-control'}))
    class Meta:
        model=Account
        fields=['first_name','last_name','email','phone_number']
    def __init__(self,*args, **kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)
        self.fields['confirm_password'].widget.attrs['placeholder']='Confirm Password'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            self.fields[field].widget.attrs['placeholder']='Confirm Password' if field=='confirm_password' else f'Enter {field}'
    def clean(self):
        clean_data=super(RegisterForm,self).clean()
        password=clean_data.get('password')
        confirm_password=clean_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not match!'
            )
class UserForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=['first_name','last_name','phone_number']
    def __init__(self,*args, **kwargs):
        super(UserForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
class UserProfileForm(forms.ModelForm):
    profile_picture=forms.ImageField(required=False,error_messages={'invalid':("Image files only")},widget=forms.FileInput)
    class Meta:
        model=UserProfile
        fields=['address_line_1','address_line_2','city','country','state','profile_picture']
    def __init__(self,*args, **kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'