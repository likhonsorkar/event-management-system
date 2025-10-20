from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from .forms import RegistrationFrom, LoginForm, CategoryForm, EventsForm
from .models import Events, Category
User = get_user_model()
def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_organizer(user):
    return user.groups.filter(name='organizer').exists()
def is_participent(user):
    return user.groups.filter(name='participent').exists()
def get_user_role(user):
    if user.groups.filter(name='admin').exists():
        return 'admin'
    elif user.groups.filter(name='organizer').exists():
        return 'organizer'
    elif user.groups.filter(name='participant').exists():
        return 'participant'
    return None
def register(request):
    if request.method == 'POST':
        form = RegistrationFrom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            form.save()
            participant_group, created = Group.objects.get_or_create(name='participant')
            user.groups.add(participant_group)
            messages.success(request, 'Registration successful. You can\'t now log in. Please check your email and active your accout to login')
            return redirect('login')
    else:
        form = RegistrationFrom()
    return render(request, 'registration.html', {'form': form})
def active_account(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Invalid activation link.")
        return redirect('login')  # redirect to login or error page
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully. You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid or has expired.")
        return redirect('login')
def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
@login_required
def role_dash(request):
    role = get_user_role(request.user)
    if role == 'admin':
        return redirect('admin_dashboard')
    elif role == 'organizer':
        return redirect('organizer_dashboard')
    elif role == 'participant':
        return redirect('participant_dashboard')
    else:
        return redirect('login')
@login_required
def admin_dashboard(request):
    user_count = User.objects.count()
    event_count = Events.objects.count()
    category_count = Category.objects.count()
    context = {
        'user_count': user_count,
        'event_count': event_count,
        'category_count': category_count,
    }
    return render(request, 'dashboard/admindashboard.html', context)
@login_required
def organizer_dashboard(request):
    events = Events.objects.filter(organizer=request.user)
    context = {
        'events': events,
    }
    return render(request, 'dashboard/organizer_dashboard.html', context)
@login_required
def participant_dashboard(request):
    events = Events.objects.filter(participants=request.user)
    context = {
        'events': events,
    }
    return render(request, 'dashboard/participant_dashboard.html', context)
def user_logout(request):
    logout(request)
    return redirect('login')
def event_home(request):
    latest_events = Events.objects.order_by('-date')[:3]
    return render(request, "home.html", {"events": latest_events})

@login_required
def join_event(request, event_id):
    event = Events.objects.get(id=event_id)
    if request.user in event.participants.all():
        messages.warning(request, "You are already participating in this event.")
    else:
        event.participants.add(request.user)
        messages.success(request, "You have successfully joined the event.")
    return redirect('event_detail', id=event_id)
@login_required
def leave_event(request, event_id):
    event = Events.objects.get(id=event_id)
    if request.user in event.participants.all():
        event.participants.remove(request.user)
        messages.success(request, "You have successfully left the event.")
    else:
        messages.warning(request, "You are not participating in this event.")
    return redirect('event_detail', id=event_id)
def is_admin_or_organizer(user):
    return user.groups.filter(name__in=['admin', 'organizer']).exists()
@login_required
@user_passes_test(is_admin_or_organizer)
def event_create(request):
    form = EventsForm(request.POST)
    if form.is_valid():
        event = form.save(commit=False)
        event.organizer = request.user
        event.save()
        messages.success(request, "Event Create Succesfull")
        return redirect("eventlist")
    return render(request, "form.html", {"form": form, "title": "Create Event"})
def event_read(request, id=None):
    if id:
        event = Events.objects.get(id=id)
        can_view_participants = is_admin(request.user) or (request.user == event.organizer)
        context = {
            'event': event,
            'can_view_participants': can_view_participants
        }
        return render(request, "event_info.html", context)
    event = Events.objects.select_related("category").prefetch_related("participants").all()
    return render(request, "event_read.html", {'events':event})
def event_detail(request, id=None):
    if id:
        event = Events.objects.get(id=id)
        can_view_participants = is_admin(request.user) or (request.user == event.organizer)
        context = {
            'event': event,
            'can_view_participants': can_view_participants
        }
        return render(request, "event_info.html", context)
    event = Events.objects.select_related("category").prefetch_related("participants").all()
    return render(request, "event_read.html", {'events':event})
@login_required
def event_update(request, id):
    event = Events.objects.get(id=id)
    if not (request.user == event.organizer or is_admin(request.user)):
        messages.error(request, "You are not authorized to update this event.")
        return redirect('eventlist')
    if request.method == "POST":
        form = EventsForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event Update Succesfull")
            return redirect("eventlist")
        else:
            messages.error(request, "Event update faild")
    else:
        form = EventsForm(instance=event)
    return render(request, "form.html", {"form": form, "title": "Update Event"})
@login_required
def event_delete(request, id):
    event = Events.objects.get(id=id)
    if not (request.user == event.organizer or is_admin(request.user)):
        messages.error(request, "You are not authorized to delete this event.")
        return redirect('eventlist')
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event Delete Succesfull")
        return redirect("eventlist")
    else:
        return render(request, "delete.html", {"object": event, "type": "Events"})
@login_required
@user_passes_test(is_admin)
def category_create(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Category Create Succesfull")
        return redirect("category_read")
    return render(request, "form.html", {"form": form, "title": "Create Category"})
def category_read(request):
    category = Category.objects.all()
    return render(request, "category_list.html", {'categories': category, 'is_admin': is_admin(request.user)})
@login_required
@user_passes_test(is_admin)
def category_update(request, id):
    category = Category.objects.get(id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category Update Succesfull")
            return redirect("category_read")
        else:
            messages.error(request, "Category update faild")
    else:
        form = CategoryForm(instance=category)
    return render(request, "form.html", {"form": form, "title": "Update Category"})
@login_required
@user_passes_test(is_admin)
def category_delete(request, id):
    category = Category.objects.get(id=id)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category Delete Succesfull")
        return redirect("category_read")
    else:
        return render(request, "delete.html", {"object": category, "type": "Category"})
@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()
    return render(request, 'dashboard/user_list.html', {'users': users})