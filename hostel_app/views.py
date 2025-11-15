from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import StudentProfile
from django.contrib.auth import logout


def register_student(request):
    if request.method == 'POST':

        roll_no = request.POST.get('roll_no')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile_no = request.POST.get('mobile_no')
        department = request.POST.get('department')
        year_of_study = request.POST.get('year_of_study')
        profile_photo = request.FILES.get('profile_photo')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register_student')

        if User.objects.filter(username=roll_no).exists():
            messages.error(request, "Roll Number already registered")
            return redirect('register_student')

        user = User.objects.create(
            username=roll_no,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name
        )

        StudentProfile.objects.create(
            user=user,
            roll_no=roll_no,
            first_name=first_name,
            last_name=last_name,
            mobile_no=mobile_no,
            department=department,
            year_of_study=year_of_study,
            profile_photo=profile_photo
        )

        messages.success(request, "Registration Successful!")
        return redirect('login')

    return render(request, 'register.html')




from django.contrib.auth import authenticate, login

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            
            if user.is_superuser:
                return redirect('admin_dashboard')

            return redirect('student_dashboard')

        messages.error(request, "Invalid Username or Password")
        return redirect('login')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

def student_dashboard(request):
    return render(request,'student_dashboard.html')
def admin_dashboard(request):
    return render(request,'admin_dashboard.html')
