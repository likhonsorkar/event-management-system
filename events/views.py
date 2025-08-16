from django.shortcuts import render,redirect
from events.models import Events,Category, Participant
from events.forms import *
from django.contrib import messages

# Create your views here.
def event_home(request):
    return render(request, "home.html")
def event_create(request):
    pass
def event_read(request):
    event = Events.objects.select_related("category").prefetch_related("participants").all()
    return render(request, "event_read.html", {'events':event})
def event_update(request):
    pass
def event_delete(request):
    pass
def participent_create(request):
    pass
def participent_read(request):
    participent = Participant.objects.all()
    return render(request, "participent_list.html", {'participents': participent})
    pass
def participent_update(request, id):
    pass
def participen_delete(request):
    pass
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