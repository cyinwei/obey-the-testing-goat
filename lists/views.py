from django.shortcuts import render


# Create your views here.
def home_page(request):
    return render(request, 'lists/home.html', {
        'todo_item_text': request.POST.get('new-todo-item-text', ''),
    })
