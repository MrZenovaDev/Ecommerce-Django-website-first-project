from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login,authenticate
from .models import UserProfile
from .forms import ProfileOfUser
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json 
# Create your views here.
def signup(request):
    if request.method=='POST':
        import json
        try:
            data=json.loads(request.body)
        except:
            data=request.POST
        form=UserCreationForm(data)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return JsonResponse({'success':True})
        
        else:
            return JsonResponse({'success':False,'errors':form.errors})
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
            next_url=request.POST.get('next') or 'product_list'
            return redirect(next_url)
    else:
        form=ProfileOfUser(instance=profile)
    return render(request,'forms/profileform.html',{'form':form})


def loginview(request):
    if request.method=='POST':
        data=json.loads(request.body)
        username=data.get('username')
        password=data.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return JsonResponse({'success':True})
        else:
            return JsonResponse({'success':False,'error':'Invalid username or password'})
    else:
        return render(request,'registration/login.html')
        