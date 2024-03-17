from django.shortcuts import render, redirect
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db() 
            user.profile.phone = form.cleaned_data.get('phone')
            user.save()
            return redirect('login')  
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_notifications(request):
    notifications = request.user.notifications.all()
    return render(request, 'notifications.html', {'notifications': notifications})
