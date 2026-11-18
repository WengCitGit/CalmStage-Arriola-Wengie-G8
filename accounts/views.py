from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .decorators import role_required
from .forms import AccountRegistrationForm, UserProfileUpdateForm
from .models import CustomUser


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f"Your CalmStage {user.get_role_display()} account has been created! Please log in."
            )
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors highlighted below.")
    else:
        form = AccountRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back to CalmStage, {user.first_name or user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You have been safely logged out of CalmStage.")
        return redirect('login')
    return redirect('dashboard')


@login_required
def dashboard_redirect_view(request):
    if request.user.role == CustomUser.Role.ADMIN:
        return redirect('admin_dashboard')
    elif request.user.role == CustomUser.Role.TEACHER:
        return redirect('teacher_dashboard')
    return redirect('student_dashboard')


@login_required
@role_required(CustomUser.Role.STUDENT)
def student_dashboard_view(request):
    context = {
        'page_title': 'Student Coping Dashboard',
        'coping_tools': [
            {
                'title': '4-7-8 Breathing Exercise',
                'desc': 'Slow your heart rate in 60 seconds before stepping on stage.',
                'badge': 'Immediate Relief',
            },
            {
                'title': 'Mock Presentation Timer',
                'desc': 'Rehearse your pacing with green, yellow, and red visual cues.',
                'badge': 'Rehearsal Tool',
            },
            {
                'title': 'CBT Reframing Cards',
                'desc': 'Replace anxious thoughts with grounded, evidence-based self-talk.',
                'badge': 'Cognitive Prep',
            },
        ]
    }
    return render(request, 'accounts/student_dashboard.html', context)


@login_required
@role_required(CustomUser.Role.TEACHER)
def teacher_dashboard_view(request):
    students = CustomUser.objects.filter(role=CustomUser.Role.STUDENT).order_by('last_name', 'first_name')
    context = {
        'page_title': 'Teacher Dashboard',
        'students': students,
        'student_count': students.count(),
    }
    return render(request, 'accounts/teacher_dashboard.html', context)


@login_required
@role_required(CustomUser.Role.ADMIN)
def admin_dashboard_view(request):
    total_students = CustomUser.objects.filter(role=CustomUser.Role.STUDENT).count()
    total_teachers = CustomUser.objects.filter(role=CustomUser.Role.TEACHER).count()
    total_admins = CustomUser.objects.filter(role=CustomUser.Role.ADMIN).count()
    recent_users = CustomUser.objects.order_by('-date_joined')[:5]

    context = {
        'page_title': 'Wellness Admin Dashboard',
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_admins': total_admins,
        'recent_users': recent_users,
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'profile_user': request.user})


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Could not update profile. Please check the errors below.")
    else:
        form = UserProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile_edit.html', {'form': form})