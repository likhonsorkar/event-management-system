from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib import messages
def is_admin(user):
    return user.groups.filter(name='admin').exists()
@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()
    return render(request, 'dashboard/user_list.html', {'users': users})
@login_required
@user_passes_test(is_admin)
def assign_role(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if request.method == 'POST':
        role = request.POST.get('group')
        organizer_group, created = Group.objects.get_or_create(name='organizer')
        participant_group, created = Group.objects.get_or_create(name='participant')
        if role == 'organizer':
            user.groups.clear()
            user.groups.add(organizer_group)
            messages.success(request, f'{user.username} has been assigned the role of Organizer.')
        elif role == 'participant':
            user.groups.clear()
            user.groups.add(participant_group)
            messages.success(request, f'{user.username} has been assigned the role of Participant.')
        else:
            messages.error(request, 'Invalid role selected.')
        return redirect('user_list')
    return render(request, 'dashboard/assign_role.html', {'user': user})