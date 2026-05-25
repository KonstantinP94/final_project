from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import forms


def sign_up(request):
   form = SignUpForm(request.POST or None)
   if request.method == "POST" and form.is_valid():
       user = form.save()
		login(request, user)
       return redirect('shop:products')
   return render(request, 'sign_up.html', {'form': form})



