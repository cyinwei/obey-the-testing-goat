from django.shortcuts import render, redirect
from lists.models import Task


def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request):
    tasks = Task.objects.all()
    return render(request, 'lists/list.html', {'tasks': tasks})


def new_list(request):
    new_item_text = request.POST['new-todo-item']
    Task.objects.create(text=new_item_text)
    return redirect('/lists/the-only-list-in-the-world/')
