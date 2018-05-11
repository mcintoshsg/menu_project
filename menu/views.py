from datetime import datetime
import pytz

from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *

# list out all menus with a date greater than 1 Jan 2016
# prefetch all items so as to spped up cliking on a single menu

def menu_list(request):
    """ list out all menus """
    last_menu_created_date = datetime(2016,1,1, tzinfo=pytz.timezone('Australia/Adelaide'))
   
    all_menus = Menu.objects.all().prefetch_related('items')
    menus = all_menus.filter(
                            expiration_date__gte=last_menu_created_date
                            ).order_by('expiration_date')
  
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})   

def menu_detail(request, pk):
    """ list out menu details """
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})

def item_detail(request, pk):
    """ list out item details """
    try: 
        item = Item.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})

def create_new_menu(request):
    """create new menu"""
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            return redirect('menu:menu_detail', pk=menu.pk)
    
    form = MenuForm()
    return render(request, 'menu/menu_new.html', {'form': form})

def edit_menu(request, pk):
    """edit a menu"""
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = MenuForm(instance=menu, data=request.POST)
        if form.is_valid:
            form.save()
            
            return redirect('menu:menu_detail', pk=pk)
    form = MenuForm(instance=menu)
    return render(request, 'menu/menu_edit.html', {'form': form})
