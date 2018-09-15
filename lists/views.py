from django.shortcuts import render, redirect
from lists.models import List, Task


def home_page(request):
    return render(request, 'lists/home.html')


def view_list(request, list_id):
    parent_list = List.objects.get(id=list_id)
    return render(request, 'lists/list.html', {'parent_list': parent_list})


def new_list(request):
    parent_list = List.objects.create()
    new_item_text = request.POST['new-todo-item']
    Task.objects.create(text=new_item_text, parent_list=parent_list)
    return redirect(f'/lists/{parent_list.id}/')


def add_task(request, list_id):
    parent_list = List.objects.get(id=list_id)
    new_item_text = request.POST['new-todo-item']
    Task.objects.create(text=new_item_text, parent_list=parent_list)
    return redirect(f'/lists/{parent_list.id}/')
