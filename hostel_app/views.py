from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from .models import StudentProfile

def register_student(request):
    if request.method == 'POST':
        roll_no = request.POST['roll_no']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        mobile_no = request.POST['mobile_no']
        department = request.POST['department']
        year_of_study = request.POST['year_of_study']

        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        profile_photo = request.FILES.get('profile_photo')

        # Password match validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # Username will be roll number (good for students)
        if User.objects.filter(username=roll_no).exists():
            messages.error(request, "Roll number already registered")
            return redirect('register')

        # Create user (password hashed)
        user = User.objects.create(
            username=roll_no,
            password=make_password(password)
        )

        # Create profile
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

        messages.success(request, "Registered successfully!")
        return redirect('login')

    return render(request, 'register.html')
