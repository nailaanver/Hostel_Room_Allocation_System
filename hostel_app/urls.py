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

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)