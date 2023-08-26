from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from datetime import datetime

# Create your views here.
def home(request):

    records = Record.objects.all()

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password= password)

        if user is not None:
            login(request, user)
            messages.success(request,'You have been successfully logged in!')
            return redirect(home)
        else:
            messages.success(request,"Something went wrong. Please try again!")
            return redirect(home)
    else:
        return render(request,'home.html', {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request,"You have been successfully logged out.")
    return redirect(home)

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            
            #Authentication
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been successfully registered.")
            return render(request, 'home.html', {'user':username})
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html',{'form':form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record, 'date': "Added n days ago"})
    else:
        messages.success(request,"You must be logged in to view the records")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_obj = Record.objects.get(id=pk)
        delete_obj.delete()
        messages.success(request,f"Record {id} deleted successfully")
        return redirect ('home')
    else:
        messages.success(request,"You must be logged in to delete the records")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request,"Record added")
                return redirect('home')

        return render(request, 'add_record.html',{'form':form})
    else:
        messages.success(request,"You must be logged in to add records!")
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        update_obj = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=update_obj)
        if form.is_valid():
            form.save()
            messages.success(request,f"Record updated...")
            return redirect ('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request,"You must be logged in to update the records")
        return redirect('home')