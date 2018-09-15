from django.shortcuts import render, redirect
from lists.models import List, Task


def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request):
    tasks = Task.objects.all()
    return render(request, 'lists/list.html', {'tasks': tasks})


def new_list(request):
    parent_list = List.objects.create()
    new_item_text = request.POST['new-todo-item']
    Task.objects.create(text=new_item_text, parent_list=parent_list)
    return redirect('/lists/the-only-list-in-the-world/')
