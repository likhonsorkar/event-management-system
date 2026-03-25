from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DetailView, DeleteView
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import CustomUser as User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from .forms import RegistrationFrom, LoginForm, CategoryForm, EventsForm, ProfileUpdateForm, UpdatePasswordForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm
from core.models import Events, Category, CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
User = get_user_model()

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='admin').exists()

def is_organizer(user):
    return user.groups.filter(name='organizer').exists()

def is_participant(user):
    return user.groups.filter(name='participant').exists()

def is_admin_or_organizer(user):
    return is_admin(user) or is_organizer(user)

def get_user_role(user):
    if is_admin(user):
        return 'admin'
    elif is_organizer(user):
        return 'organizer'
    elif is_participant(user):
        return 'participant'
    return None

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def register(request):
    if request.method == 'POST':
        form = RegistrationFrom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            messages.success(request, 'Registration successful. Please check your email to activate your account.')
            return redirect('login')
    else:
        form = RegistrationFrom()
    return render(request, 'registration.html', {'form': form})

def active_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
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
                # Check if user exists but is inactive
                user_model = get_user_model()
                try:
                    target_user = user_model.objects.get(username=username)
                    if not target_user.is_active:
                        messages.error(request, 'Your account is not active. Please check your email for the activation link.')
                    else:
                        messages.error(request, 'Invalid username or password.')
                except user_model.DoesNotExist:
                    messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

from django.utils import timezone

@login_required
@user_passes_test(is_admin)
def approve_event(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    event.is_approved = True
    event.save()
    messages.success(request, f'Event "{event.name}" has been approved.')
    return redirect('dashboard')

@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        return redirect('dashboard')
        
    context = {
        'total_users': User.objects.count(),
        'total_events': Events.objects.count(),
        'total_categories': Category.objects.count(),
        'upcoming_events': Events.objects.filter(date__gte=timezone.now(), is_approved=True).count(),
        'pending_approvals': Events.objects.filter(is_approved=False).count(),
        'recent_events': Events.objects.all().order_by('-id')[:5],
        'pending_events': Events.objects.filter(is_approved=False).order_by('-id'),
        'title': 'Admin Overview'
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def dashboard_view(request):
    if is_admin(request.user):
        return admin_dashboard(request)
        
    role = get_user_role(request.user)
    
    if role == 'organizer':
        events = Events.objects.filter(organizer=request.user)
        context = {
            'total_events': events.count(),
            'total_users': sum(e.participants.count() for e in events),
            'total_categories': events.values('category').distinct().count(),
            'upcoming_events': events.filter(date__gte=timezone.now(), is_approved=True).count(),
            'recent_events': events.order_by('-id')[:5],
            'title': 'Organizer Overview'
        }
    else: # participant or default
        events = Events.objects.filter(participants=request.user)
        context = {
            'total_events': events.count(),
            'total_users': 0,
            'total_categories': events.values('category').distinct().count(),
            'upcoming_events': events.filter(date__gte=timezone.now(), is_approved=True).count(),
            'recent_events': events.order_by('-id')[:5],
            'title': 'Member Overview'
        }
        
    return render(request, 'dashboard/index.html', context)

def user_logout(request):
    logout(request)
    return redirect('login')

def event_home(request):
    latest_events = Events.objects.filter(is_approved=True).order_by('-date')[:3]
    total_events = Events.objects.filter(is_approved=True).count()
    total_users = CustomUser.objects.count()
    total_categories = Category.objects.count()
    # For countries, we'll use a unique count of locations if it's formatted as 'City, Country' 
    # but since it's a simple CharField, we can just show a meaningful static-ish or count unique locations.
    total_locations = Events.objects.values('location').distinct().count()
    
    context = {
        "events": latest_events,
        "total_events": total_events,
        "total_users": total_users,
        "total_categories": total_categories,
        "total_locations": total_locations,
    }
    return render(request, "home.html", context)

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    if request.user == event.organizer:
        messages.error(request, "You cannot join your own event.")
    elif request.user in event.participants.all():
        messages.warning(request, "You are already participating in this event.")
    else:
        event.participants.add(request.user)
        messages.success(request, "You have successfully joined the event.")
    return redirect('event_detail', id=event_id)

@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    if request.user in event.participants.all():
        event.participants.remove(request.user)
        messages.success(request, "You have successfully left the event.")
    else:
        messages.warning(request, "You are not participating in this event.")
    return redirect('event_detail', id=event_id)

class EventCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView ):
    permission_denied_message = "Only organizers and admins can create events."
    model = Events
    form_class = EventsForm
    template_name = "form.html"
    success_url = reverse_lazy("manage_events")
    def test_func(self):
       return is_admin_or_organizer(self.request.user)
    def form_valid(self, form):
        event = form.save(commit=False)
        event.organizer = self.request.user
        if not is_admin(self.request.user):
            event.is_approved = False 
        else:
            event.is_approved = True 
        event.save()
        messages.success(self.request, "Event Create Successful" if event.is_approved else "Event created successfully and is pending approval.")
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create Event"
        context["base_template"] = "dashboard/base.html" if self.request.user.is_authenticated else "template.html"
        return context

class EventRead(ListView):
    model = Events
    template_name = "event_read.html"
    context_object_name = 'events'

    def get_queryset(self):
        queryset = Events.objects.filter(is_approved=True).select_related("category").prefetch_related("participants")
        
        search_query = self.request.GET.get('search')
        category_id = self.request.GET.get('category')

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        return queryset.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["base_template"] = "dashboard/base.html" if self.request.user.is_authenticated else "template.html"
        return context

class ManageEvents(LoginRequiredMixin, ListView):
    model = Events
    template_name = "dashboard/event_list.html"
    context_object_name = 'events'
    
    def get_queryset(self):
        user = self.request.user
        if is_admin(user):
            return Events.objects.select_related("category").prefetch_related("participants").all()
        return Events.objects.filter(organizer=user).select_related("category").prefetch_related("participants")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["base_template"] = "dashboard/base.html"
        return context
    
class Event_detail(DetailView):
    model = Events
    pk_url_kwarg = 'id'
    template_name = "event_info.html"
    context_object_name = 'event'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        context['can_view_participants'] = is_admin(self.request.user) or (self.request.user == event.organizer)
        context["base_template"] = "template.html"
        return context

class Event_update(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    permission_denied_message = "You are not authorized to update this event."
    model = Events
    form_class = EventsForm
    context_object_name = "event"
    pk_url_kwarg = 'id'
    template_name = "form.html"
    def test_func(self):
       event = self.get_object()
       return is_admin(self.request.user) or self.request.user == event.organizer
    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect('manage_events')
    def get_success_url(self):
        messages.success(self.request, "Event Update Successful")
        return reverse_lazy('manage_events')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Update Event"
        context["base_template"] = "dashboard/base.html" if self.request.user.is_authenticated else "template.html"
        return context

class EventDelete(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Events
    template_name = "delete.html"
    permission_denied_message = "You are not authorized to delete this event."
    success_url = reverse_lazy("manage_events")
    pk_url_kwarg = 'id'
    context_object_name = 'event'

    def test_func(self):
       event = self.get_object()
       return is_admin(self.request.user) or self.request.user == event.organizer
    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect('manage_events')
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Event Delete Successful")
        return super().delete(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Events"
        context["base_template"] = "dashboard/base.html" if self.request.user.is_authenticated else "template.html"
        return context

@login_required
@user_passes_test(is_admin)
def category_create(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category Create Successful")
        return redirect("category_read")
    return render(request, "form.html", {"form": form, "title": "Create Category", "base_template": "dashboard/base.html"})

@login_required
@user_passes_test(is_admin)
def category_read(request):
    category = Category.objects.all()
    return render(request, "category_list.html", {'categories': category, 'is_admin': True, 'base_template': "dashboard/base.html"})

@login_required
@user_passes_test(is_admin)
def category_update(request, id):
    category = get_object_or_404(Category, id=id)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Category Update Successful")
        return redirect("category_read")
    return render(request, "form.html", {"form": form, "title": "Update Category", "base_template": "dashboard/base.html"})

@login_required
@user_passes_test(is_admin)
def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category Delete Successful")
        return redirect("category_read")
    return render(request, "delete.html", {"object": category, "type": "Category", "base_template": "dashboard/base.html"})

@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()
    return render(request, 'dashboard/user_list.html', {'users': users})

#Profile
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile/profile.html"
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = "profile/update_profile.html"
    success_url = reverse_lazy("profile")
    def get_object(self):
        return self.request.user
class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "profile/password.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy("password_change_done")
    def form_invalid(self, form):
        messages.error(self.request, "Form is invalid or password requirement not meet")
        return super().form_invalid(form)
    
class ChangePasswordDone(PasswordChangeDoneView):
    template_name = "profile/password_done.html"

class UserPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'password_reset.html'
    success_url = reverse_lazy('login')
    html_email_template_name = 'reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.conf import settings
        context['protocol'] = settings.SITE_PROTOCOL
        context['domain'] = settings.SITE_DOMAIN
        return context

    def form_valid(self, form):
        messages.success(
            self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'password_reset.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)
