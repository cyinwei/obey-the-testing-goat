from django.shortcuts import render, redirect
from lists.models import Item


def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['new-todo-item']
        Item.objects.create(text=new_item_text)
        return redirect('/')

    return render(request, 'lists/home.html')
