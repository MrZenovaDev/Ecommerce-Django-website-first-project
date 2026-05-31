from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login
from .models import UserProfile
from .forms import ProfileOfUser
from django.contrib.auth.decorators import login_required
# Create your views here.
def signup(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('product_list')
        
    else:
        form=UserCreationForm()
    return render(request,'registration/signup.html',{'form':form})
@login_required
def profileform(request):
    profile,created=UserProfile.objects.get_or_create(user=request.user)
    if request.method=='POST':
        form=ProfileOfUser(request.POST,instance=profile)
        if form.is_valid():
            profile=form.save(commit=False)
            profile.user=request.user
            profile.save()
            return redirect('product_list')
    else:
        form=ProfileOfUser(instance=profile)
    return render(request,'forms/profileform.html',{'form':form})

