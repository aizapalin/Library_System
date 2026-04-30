from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Member
from .forms import MemberForm
from accounts.decorators import librarian_required

# --- READ (List) ---
@login_required
@librarian_required
def member_index(request):
    members = Member.objects.all().order_by('-date_joined')
    return render(request, 'members/index.html', {'members': members})

# --- CREATE (Librarian Only) ---
@login_required
@librarian_required
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('members:index')
    else:
        form = MemberForm()
    return render(request, 'members/add.html', {'form': form})

# --- UPDATE (Librarian Only) ---
@login_required
@librarian_required
def edit_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('members:index')
    else:
        form = MemberForm(instance=member)
    return render(request, 'members/edit.html', {'form': form, 'member': member})

# --- DELETE (Librarian Only) ---
@login_required
@librarian_required
def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('members:index')
    return render(request, 'members/delete.html', {'member': member})

# --- REGISTRATION (Public) ---
def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_management:index')
    else:
        form = UserCreationForm()
    return render(request, 'members/register.html', {'form': form})