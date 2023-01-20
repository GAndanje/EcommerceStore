from django.core.mail import EmailMessage
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import RegisterForm
from .models import Account
from Cart.models import Cart,CartItem
from Cart.views import _get_session_id

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import requests
# Create your views here.
def register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            phone_number=form.cleaned_data['phone_number']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password'] 
            username=email.split('@')[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()
            # user activation
            current_site=get_current_site(request)
            mail_subject='Please verify your email'
            message=render_to_string('accounts/accounts_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
                })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            
            # messages.success(request,'We have sent you a verification email kindly confirm to activate your account!')
            return redirect(f"/accounts/Login/?command=verification&email={email}")
    else:
        form=RegisterForm()
    context={
        'form':form
    }
    return render(request,'accounts/register.html',context)

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(request,email=email,password=password)
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_get_session_id(request))
                print(request.session.session_key)
                cart_item_exists=CartItem.objects.filter(cart=cart).exists()
                if cart_item_exists:
                    cart_items=CartItem.objects.filter(cart=cart)
                    product_variation_list=[]
                    for item in cart_items:
                        variations=item.product_variation.all()
                        product_variation_list.append(list(variations))
                        print(list(product_variation_list))
                    cart_items=CartItem.objects.filter(user=user)
                    existing_variation_list=[]
                    id=[]
                    for item in cart_items:
                        variations=item.product_variation.all()
                        existing_variation_list.append(list(variations))
                        id.append(item.id)
                        print(id)
                    for item in product_variation_list:
                        if item in existing_variation_list:
                            index=existing_variation_list.index(item)
                            print('index: ',index )
                            item_id=id[index]
                            print('id: ',item_id )
                            item=CartItem.objects.get(id=item_id)
                            item.quantity+=1
                            item.user=user
                            item.save()
                        else:
                            cart_items= CartItem.objects.filter(cart=cart)
                            for cart_item in cart_items:
                                cart_item.user=user
                                cart_item.save()
            except:
                pass
            auth.login(request,user)
            messages.success(request,'You are now logged in!')
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid Password or/and Email')
            return redirect('login')
    return render(request,'accounts/login.html')
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out.')
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(ValueError,OverflowError,Account.DoesNotExist,TypeError):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,'Your account is now active!')
        return redirect('login')
    else:
        messages.error(request,'Link has expired')
        return redirect('register')

@login_required
def dashboard(request):
    context=None
    return render(request,'accounts/dashboard.html',context)

def forgotPassword(request):
    if request.method=='POST':
        email=request.POST['email']
        user_exists=Account.objects.filter(email=email).exists()
        if user_exists:
            user=Account.objects.get(email__exact=email)
            current_site=get_current_site(request)
            mail_subject='Please reset password'
            message=render_to_string('accounts/reset_password.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
                })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'reset link has been sent to your email. Please check your mail for a password reset link')
            return redirect('login')
    
        else:
            messages.error(request,'account does not exist')
            return redirect('forgotPassword')
    return render(request,'accounts/forgotPassword.html')

def reset_password_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(ValueError,OverflowError,Account.DoesNotExist,TypeError):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request,'This link is expired')
        return redirect('login')

def resetPassword(request):
    if request.method=='POST':
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successful!')
            return redirect('login')
        else:
            messages.error(request,'passwords do not match!')
            return redirect('resetPassword')
    return render(request,'accounts/resetPasswordForm.html')