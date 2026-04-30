from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import BorrowRecord
from .forms import BorrowForm
from book_management.models import Book
from accounts.decorators import librarian_required

# --- READ INDEX ---
@login_required
@librarian_required
def borrow_index(request):
    status = request.GET.get("status", "All").strip().lower()
    today = timezone.localdate()

    # Keep overdue records accurate for active loans past due date.
    BorrowRecord.objects.filter(status="Active", due_date__lt=today).update(status="Overdue")

    records = BorrowRecord.objects.select_related(
        "book", "member", "book__author", "book__category", "book__details"
    ).all()

    if status == "active":
        records = records.filter(status="Active").exclude(due_date__lt=today)
    elif status == "overdue":
        records = records.filter(status__in=["Active", "Overdue"], due_date__lt=today)
    elif status in ("returned", "completed"):
        records = records.filter(status="Returned")
    elif status == "pending":
        records = records.filter(status="Pending")
    # "All" => keep all

    # For the template we always pass through the raw records queryset;
    # overdue labels are still computed in BorrowRecord.is_overdue.
    return render(request, 'borrow/index.html', {'records': records})


@login_required
@librarian_required
def request_detail(request, pk):
    record = get_object_or_404(
        BorrowRecord.objects.select_related(
            "book", "member", "book__author", "book__category", "book__details"
        ),
        pk=pk,
    )
    return render(request, "borrow/request_detail.html", {"record": record})


@login_required
@librarian_required
def update_status(request, pk, action):
    if request.method != "POST":
        return redirect("borrow:borrow_index")

    record = get_object_or_404(BorrowRecord, pk=pk)

    if action == "accept" and record.status == "Pending":
        record.status = "Active"
        record.save(update_fields=["status"])
    elif action == "decline" and record.status == "Pending":
        record.status = "Declined"
        record.save(update_fields=["status"])
    elif action == "return" and record.status in ["Active", "Overdue", "Accepted"]:
        record.status = "Returned"
        record.return_date = timezone.localdate()
        record.save(update_fields=["status", "return_date"])

    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("borrow:borrow_index")

# --- THE BORROW STATION (Combined logic) ---
@login_required
@librarian_required
def add_borrow(request):
    book = None
    isbn_query = request.GET.get('isbn_search')
    
    if isbn_query:
        book = Book.objects.filter(isbn=isbn_query).first()

    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('borrow:borrow_index')
    else:
        # Pre-select the book if found via ISBN search
        initial_data = {'book': book.id} if book else {}
        form = BorrowForm(initial=initial_data)

    return render(request, 'borrow/add.html', {
        'form': form,
        'found_book': book,
        'isbn_query': isbn_query
    })

# --- UPDATE (Returning a book) ---
@login_required
@librarian_required
def edit_borrow(request, pk):
    record = get_object_or_404(BorrowRecord, pk=pk)
    
    if request.method == 'POST':
        form = BorrowForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('borrow:borrow_index')
    else:
        form = BorrowForm(instance=record)

    # CHANGE THIS to 'borrow/add.html' to match your existing file
    return render(request, 'borrow/add.html', {
        'form': form,
        'record': record,
        'editing': True
    })

# --- DELETE ---
@login_required
@librarian_required
def delete_borrow(request, pk):
    # This looks for the record. If it was already deleted, it throws the 404.
    record = get_object_or_404(BorrowRecord, pk=pk)
    
    if request.method == 'POST':
        record.delete()
        return redirect('borrow:borrow_index')
    
    # If you don't have a separate delete.html, just redirect back
    return redirect('borrow:borrow_index')