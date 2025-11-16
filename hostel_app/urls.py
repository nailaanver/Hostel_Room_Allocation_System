from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from hostel_app import views

urlpatterns = [
    path('',views.login_user,name='login'),
    path('register_student/',views.register_student,name='register_student'),
    path('student_dashboard/',views.student_dashboard,name='student_dashboard'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('logout/', views.logout_user, name='logout'),
    path('assign-room/<int:student_id>/', views.assign_room_to_student, name='assign_room_to_student'),
    
# ROOM MANAGEMENT
    path("rooms/", views.room_list, name="room_list"),
    path("rooms/add/", views.add_room, name="add_room"),
    path("rooms/edit/<int:room_id>/", views.edit_room, name="edit_room"),
    path("rooms/delete/<int:room_id>/", views.delete_room, name="delete_room"),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)