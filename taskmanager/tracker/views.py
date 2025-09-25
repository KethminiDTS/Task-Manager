from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm, TaskForm
from .models import User, Task
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv
from datetime import date
from .forms import EmailLoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['role'] == 'manager' and User.objects.filter(role='manager').exists():
                form.add_error('role', 'Only one manager allowed.')
            else:
                form.save()
                return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'tracker/register.html', {'form': form})

def login_view(request):
    form = EmailLoginForm()
    error = None
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['office_email']
            password = form.cleaned_data['password']
            user = authenticate(request, office_email=email, password=password)
            if user:
                login(request, user)
                return redirect('submit' if user.role == 'employee' else 'dashboard')
            else:
                error = "Invalid email or password."
    return render(request, 'tracker/login.html', {'form': form, 'error': error})

class RoleBasedLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.role == 'manager':
            return reverse_lazy('dashboard')  # Manager dashboard
        elif user.role == 'employee':
            return reverse_lazy('submit')  # Employee task form
        return reverse_lazy('home')  # Fallback
    

def role_based_logout(request):
    if request.user.is_authenticated:
        user_role = request.user.role
        logout(request)

        if user_role == 'manager':
            return redirect('login')  # Or a special manager logout page
        else:
            return redirect('home')  # Employee or public home page
    else:
        return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('/')


def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'manager':
            return redirect('dashboard')
        else:
            return redirect('submit')
    return render(request, 'tracker/home.html')

@login_required
def task_submit(request):
    tasks = Task.objects.filter(user=request.user).order_by('-date')
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('submit')
    return render(request, 'tracker/task_form.html', {'form': form, 'tasks': tasks})

@login_required
def manager_dashboard(request):
    if request.user.role != 'manager':
        return redirect('home')

    # Get all employees for the filter dropdown
    employees = User.objects.filter(role='employee').order_by('first_name')

    # Get filter values from GET parameters
    selected_date = request.GET.get('date')
    selected_employee = request.GET.get('employee')

    tasks = Task.objects.all().order_by('-date')

    # Apply filters
    if selected_date:
        tasks = tasks.filter(date=selected_date)
    if selected_employee:
        tasks = tasks.filter(user_id=selected_employee)

    context = {
        'tasks': tasks,
        'employees': employees,
        'selected_date': selected_date,
        'selected_employee': selected_employee,
    }
    return render(request, 'tracker/dashboard.html', context)

@login_required
def export_csv(request):
    if request.user.role != 'manager':
        return redirect('home')

    selected_date = request.GET.get('date')
    selected_employee = request.GET.get('employee')

    tasks = Task.objects.all()

    if selected_date:
        tasks = tasks.filter(date=selected_date)
    if selected_employee:
        tasks = tasks.filter(user_id=selected_employee)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response, quoting=csv.QUOTE_ALL)

    writer.writerow([
        'Date', 'Priority', 'District', 'Module', 'Task', 'Details',
        'Target Date', 'Status', 'Live', 'Tested', 'Completed Date', 'Comments', 'Employee'
    ])

    for task in tasks:
        writer.writerow([
            task.date.strftime('%m/%d/%Y') if task.date else '',
            task.priority,
            task.district,
            task.module,
            task.task,
            task.details,
            task.target_date.strftime('%m/%d/%Y') if task.target_date else '',
            task.status,
            task.live,
            task.tested,
            task.completed_date.strftime('%m/%d/%Y') if task.completed_date else '',
            task.comments,
            task.user.first_name
        ])

    return response

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('submit')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tracker/edit_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('submit')
    return render(request, 'tracker/delete_task.html', {'task': task})

@login_required
def employee_list(request):
    if request.user.role != 'manager':
        return redirect('home')

    employees = User.objects.filter(role='employee').order_by('first_name', 'last_name')

    context = {
        'employees': employees
    }
    return render(request, 'tracker/employee_list.html', context)

def edit_employee(request, user_id):
    if request.user.role != 'manager':
        return redirect('home')

    user = get_object_or_404(User, id=user_id, role='employee')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        messages.success(request, "Employee updated successfully.")
        return redirect('employee_list')

    return render(request, 'tracker/edit_employee.html', {'employee': user})


@login_required
def delete_employee(request, user_id):
    if request.user.role != 'manager':
        return redirect('home')

    user = get_object_or_404(User, id=user_id, role='employee')
    user.delete()
    messages.success(request, "Employee deleted successfully.")
    return redirect('employee_list')