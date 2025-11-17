from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import StudentProfile,Room,Allocation
from django.contrib.auth import logout
from django.db import models
from django.db.models import F




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
    total_rooms = Room.objects.count()
    occupied_rooms = Room.objects.filter(current_occupancy__gte=1).count()
    vacant_rooms = Room.objects.filter(current_occupancy__lt=models.F('capacity')).count()

    total_students = StudentProfile.objects.count()

    recent_allocations = Allocation.objects.order_by('-created_at')[:5]

    available_rooms = Room.objects.filter(current_occupancy__lt=F('capacity'))
    for r in available_rooms:
        r.remaining_beds = r.capacity - r.current_occupancy


    students = StudentProfile.objects.all()

    return render(request, "admin_dashboard.html", {
        "total_rooms": total_rooms,
        "occupied_rooms": occupied_rooms,
        "vacant_rooms": vacant_rooms,
        "total_students": total_students,
        "recent_allocations": recent_allocations,
        "available_rooms": available_rooms,
        "students": students,
    })

def assign_room_to_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)

    # Only show rooms that have space
    rooms = Room.objects.filter(current_occupancy__lt=F('capacity'))

    if request.method == "POST":
        room_id = request.POST.get("room_id")
        room = get_object_or_404(Room, id=room_id)

        # 1️⃣ Check if student already has a room
        if student.room:
            messages.error(request, "Student already has a room assigned!")
            return redirect('assign_room', student_id=student_id)

        # 2️⃣ Check if room is full
        if room.current_occupancy >= room.capacity:
            messages.error(request, "Room is already full!")
            return redirect('assign_room', student_id=student_id)

        # 3️⃣ Assign room properly
        room.current_occupancy += 1
        room.save()

        student.room = room
        student.save()

        Allocation.objects.create(
            student=student,
            room=room,
            allocated_by=request.user
        )

        messages.success(request, "Room assigned successfully!")
        return redirect('admin_dashboard')

    return render(request, 'assign_room.html', {
        'student': student,
        'rooms': rooms
    })

def reassign_room(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    rooms = Room.objects.filter(current_occupancy__lt=F('capacity'))

    if request.method == "POST":
        old_room = student.room  # previous room

        room_id = request.POST.get("room_id")
        new_room = get_object_or_404(Room, id=room_id)

        # decrease old room occupancy
        if old_room:
            old_room.current_occupancy -= 1
            old_room.save()

        # increase new room occupancy
        new_room.current_occupancy += 1
        new_room.save()

        # update student
        student.room = new_room
        student.save()

        # save allocation history
        Allocation.objects.create(
            student=student,
            room=new_room,
            allocated_by=request.user
        )

        return redirect('admin_dashboard')

    return render(request, 'reassign_room.html', {
        'student': student,
        'rooms': rooms,
    })


# room management

def add_room(request):
    if request.method == "POST":
        room_number = request.POST.get("room_number")
        room_type = request.POST.get("room_type")
        capacity = request.POST.get("capacity")

        Room.objects.create(
            room_number=room_number,
            room_type=room_type,
            capacity=capacity
        )

        return redirect('room_list')

    return render(request, "add_room.html")

def room_list(request):
    rooms = Room.objects.all()
    return render(request, "room_list.html", {"rooms": rooms})

def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        room.room_number = request.POST.get("room_number")
        room.room_type = request.POST.get("room_type")
        room.capacity = request.POST.get("capacity")
        room.save()

        return redirect("room_list")

    return render(request, "edit_room.html", {"room": room})


def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    return redirect("room_list")


