from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomCreationForm

# my views

def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = auth.authenticate(username = username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Invalid Credentials! Please try again.')
            return redirect('loginUser')

    return render(request, 'loginUser.html')

def registerUser(request):
    form = CustomCreationForm()

    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if password1 == password2:
                user = auth.authenticate(email = email, username=username, password = password1)

                if user is not None:
                    login(request, user)
                    return redirect('store')
                else:
                    messages.info(request, 'Invalid Credentials! Please try again.')
                    return redirect('loginUser')
            else:
                messages.info(request, 'Enter a valid password!')
                return redirect('loginUser') 
            
    context = {'form': form}             
    return render(request, 'registerUser.html', context)

def logoutUser(request): #logout user view
    logout(request)
    return redirect('loginUser')