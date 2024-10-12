import csv
import logging
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.db.models import Count
from .models import Archive
from .forms import ArchiveForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.core.paginator import Paginator


import logging
logger = logging.getLogger(__name__)


@login_required
def archive_form(request):
    if request.method == 'POST':
        form = ArchiveForm(request.POST)
        if form.is_valid():
            archive = form.save(commit=False)
            archive.user = request.user
            archive.save()
            messages.success(request, "Archive added successfully.")
            return redirect('archive_success')
    else:
        form = ArchiveForm()
    return render(request, 'archiver/archive.html', {'form': form})


def archive_success(request):
    

    return render(request, 'archiver/archive_success.html')


@login_required
def view_archives(request):
    
    query = request.GET.get('search', '')
    if request.user.is_superuser:  
        archives = Archive.objects.all()  
    else:
        
        archives = Archive.objects.filter(user=request.user)

    if query:
        archives = archives.filter(title__icontains=query) | archives.filter(
            content__icontains=query)

    paginator = Paginator(archives, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    archives_per_month = archives.annotate(month=TruncMonth('created_at')).values(
        'month').annotate(count=Count('id')).order_by('month')
    labels = [archive['month'].strftime('%Y-%m')
              for archive in archives_per_month]
    data = [archive['count'] for archive in archives_per_month]

    context = {
        'page_obj': page_obj,
        'labels': labels,
        'data': data,
    }

    return render(request, 'archiver/view_archives.html', context)


@login_required
@require_http_methods(["POST"])
def clear_archives(request):
   
    if request.user.is_authenticated:
        if request.user.is_superuser: 
            Archive.objects.all().delete()
        else:
            Archive.objects.filter(user=request.user).delete()
        messages.success(
            request, "All your archives have been cleared successfully!")
        return redirect('view_archives')
    else:
        messages.error(request, "You need to be logged in to clear archives.")
        return redirect('login')


def export_archives_csv(request):
    
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="archives.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Title', 'Content', 'Created At', 'Category', 'Tags'])

    archives = Archive.objects.all()
    for archive in archives:
        writer.writerow([archive.title, archive.content,
                        archive.created_at.strftime("%Y-%m-%d %H:%M:%S")])

    return response


def reg(request):
  
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('archive-view')
    else:
        form = UserCreationForm()
    return render(request, 'archiver/reg/register.html', {'form': form})


@login_required
def archive_view(request):
    return render(request, 'archiver/archive.html')


@login_required
def about_us(request):
    return render(request, 'archiver/aboutus.html')
