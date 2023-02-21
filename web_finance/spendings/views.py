from django.shortcuts import render, redirect
from .models import *
from .forms import *
from datetime import datetime
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse
import csv
from django.core.paginator import Paginator
from django.db.models import Q


def spendigs_view(request, id):
    myuser = User.objects.get(id=id)
    allcategories = categories.objects.all().values()
    print(request.GET)
    searched_id = []
    for cat in allcategories: 
        if ('q' in request.GET) and (request.GET['q'].lower() in cat['description'].lower()):
            searched_id.append(cat['id'])
        else:
            searched_id.append(cat['id'])

    myuserspendings = spendings.objects.filter(Q(user=myuser) & Q(category__in=searched_id)).order_by('-date').values()
    # set up paginator, 6 spendings per page
    p = Paginator(spendings.objects.filter(Q(user=myuser) & Q(category__in=searched_id)).order_by('-date').values(), 6)

    page = request.GET.get('page')
    spendings_page = p.get_page(page)
    nums = "a" * spendings_page.paginator.num_pages
    nums_ge_6 = spendings_page.paginator.num_pages > 6
    last_num_page = spendings_page.paginator.num_pages
    prelast_num_page = spendings_page.paginator.num_pages - 1
    preprelast_num_page = spendings_page.paginator.num_pages - 2
    
    context = {
        'myuser': myuser,
        'myuserspendings': myuserspendings,
        'allcategories': allcategories,
        'spendings_page': spendings_page,
        'nums': nums,
        'nums_ge_6': nums_ge_6,
        'last_num_page': last_num_page,
        'prelast_num_page': prelast_num_page,
        'preprelast_num_page': preprelast_num_page
    }
    return render(request, 'spendings/list_spendings.html', context)


def add_spending(request):
    if request.method == 'POST':
        form = SpendingForm(request.POST)
        if form.is_valid():
            print('form valid', request.POST)
            form.save()
            return redirect('spendings',request.user.id)
        else:
            print('form invalid', request.POST)
    else:
        form = SpendingForm(initial={'user': f'{request.user.id}'})

    context = {
        'form': form,
    }
    return render(request, 'spendings/add_spending.html', context)


def editspending(request, id):
    myspending = spendings.objects.get(id = id)
    form = SpendingForm(request.POST or None, instance=myspending)
    if form.is_valid():
        form.save()
        return redirect('spendings',request.user.id)
        
    context = {
        'form': form,
        'myspending': myspending,
    }
    return render(request, 'spendings/edit_spending.html', context)


def deletespending(request, id):
    myspending = spendings.objects.get(id = id)
    myspending.delete()
    messages.success(request, ("Spending was deleted"))
    return redirect('spendings',request.user.id)


def spendingscsv(request):
    responce = HttpResponse(content_type='text/csv')
    responce['Content-Disposition'] = 'attachment; filename=spendings.csv'

    writer = csv.writer(responce)

    myuserspendings = spendings.objects.filter(user = request.user.id).values()
    allcategories = categories.objects.all().values()

    writer.writerow(['id', 'date', 'amount', 'category', 'user'])

    for spending in myuserspendings:
        print(spending)
        cat_id = spending['category_id'] - 1 
        writer.writerow([spending['id'], spending['date'], spending['amount'], allcategories[cat_id]['description'], request.user])

    return responce

def add_category(request):
    allcategories = categories.objects.all().values()
    bad = False
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        for cat in allcategories: 
            if request.POST['description'].lower() == cat['description'].lower():
                bad = True
        if form.is_valid() and not bad:
            print('form valid', request.POST)
            form.save()
            return redirect('add_spending')
        else:
            if bad:
                messages.success(request, ("Category alredy exist"))
            print('form invalid', request.POST)
    else:
        form = CategoryForm()

    

    context = {
        'form': form,
        'allcategories': allcategories
    }
    return render(request, 'spendings/add_category.html', context)

def delete_category(request, id):
    mycategory = categories.objects.get(id = id)
    mycategory.delete()
    messages.success(request, ("Category was deleted"))
    return redirect('add_category')


