from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from lists.forms import ItemForm
from lists.models import Item, List

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            Item.objects.create(text=request.POST['text'], list=list)
            return redirect('/lists/%d/' % (list.id,))
        except ValidationError as e:
            if 'blank' in str(e):
                error = "You can't have an empty list item"
            elif 'already exists' in str(e):
                error = "You've already got this in your list"

    return render(request, 'list.html', {'list': list, "error": error})


def new_list(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        list = List.objects.create()
        Item.objects.create(text=form.cleaned_data['text'], list=list)
        return redirect('/lists/%d/' % (list.id,))
    return render(request, 'home.html', {'form': form})

