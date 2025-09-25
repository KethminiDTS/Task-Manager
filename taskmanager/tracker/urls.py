from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('submit/', views.task_submit, name='submit'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('dashboard/', views.manager_dashboard, name='dashboard'),
    path('export/', views.export_csv, name='export_csv'),
    path('login/', views.RoleBasedLoginView.as_view(), name='login'),
    path('logout/', views.role_based_logout, name='logout'),
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/edit/<int:user_id>/', views.edit_employee, name='edit_employee'),
    path('employees/delete/<int:user_id>/', views.delete_employee, name='delete_employee'),
]