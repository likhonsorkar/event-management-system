from django.shortcuts import render,redirect
from events.models import Events,Category, Participant
from events.forms import *
from django.contrib import messages
# Create your views here.
def event_home(request):
    event = Events.objects.select_related('category').prefetch_related('participants').all()
    return render(request, "home.html", {"coming_soon": event})
def event_detail(request, id):
    event = Events.objects.get(id=id)
    return render(request, "event_info.html", {"event": event})
def event_create(request):
    form = EventsForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Event Create Succesfull")
        return redirect("eventlist")
    return render(request, "form.html", {"form": form, "title": "Create Event"})
def event_read(request):
    event = Events.objects.select_related("category").prefetch_related("participants").all()
    return render(request, "event_read.html", {'events':event})
def event_update(request, id):
    event = Events.objects.get(id=id)
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
def event_delete(request, id):
    event = Events.objects.get(id=id)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event Delete Succesfull")
        return redirect("eventlist")
    else:
        return render(request, "delete.html", {"object": event, "type": "Events"})
def participent_create(request):
    form = ParticipantForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Participent Create Succesfull")
        return redirect("participent_read")
    return render(request, "form.html", {"form": form, "title": "Create Participent"})
def participent_read(request):
    participent = Participant.objects.prefetch_related('events').all()
    return render(request, "participent_list.html", {'participents': participent})
def participent_update(request, id):
    participent = Participant.objects.get(id=id)
    if request.method == "POST":
        form = ParticipantForm(request.POST, instance=participent)
        if form.is_valid():
            form.save()
            messages.success(request, "Perticcipent Update Succesfull")
            return redirect("participent_read")
        else:
            messages.error(request, "Participent update faild")
    else:
        form = ParticipantForm(instance=participent)
    return render(request, "form.html", {"form": form, "title": "Update Participent"})
def participen_delete(request, id):
    participent = Participant.objects.get(id=id)
    if request.method == "POST":
        participent.delete()
        messages.success(request, "Participent Delete Succesfull")
        return redirect("participent_read")
    else:
        return render(request, "delete.html", {"object": participent, "type": "Participents"})
def category_create(request):
    form = CategoryForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Category Create Succesfull")
        return redirect("category_read")
    return render(request, "form.html", {"form": form, "title": "Create Category"})
def category_read(request):
    category = Category.objects.all()
    return render(request, "category_list.html", {'categories': category})
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
def category_delete(request, id):
    category = Category.objects.get(id=id)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category Delete Succesfull")
        return redirect("category_read")
    else:
        return render(request, "delete.html", {"object": category, "type": "Category"})