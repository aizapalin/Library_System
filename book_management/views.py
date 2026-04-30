from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils import timezone
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
import re
from .models import Book, Author, BookDetails, Category 
from borrow.models import BorrowRecord
from members.models import Member
from accounts.decorators import librarian_required
from .forms import LibrarianRegisterForm

User = get_user_model()

# This view renders the main catalog page for librarians and members.
@login_required
def index(request):
    role = getattr(request.user, "role", "guest")
    is_librarian = request.user.is_staff or request.user.is_superuser or role == "librarian"

    if is_librarian:
        query = request.GET.get("q", "").strip()
        books = Book.objects.select_related("author", "category", "details").all().order_by("category__name", "title")
        if query:
            books = books.filter(
                Q(title__icontains=query)
                | Q(author__name__icontains=query)
                | Q(category__name__icontains=query)
                | Q(details__isbn__icontains=query)
            )
        return render(request, "book_management/index.html", {"books": books, "query": query})

    # This branch handles member-facing search and filtering behavior.
    query = request.GET.get("q", "").strip()
    title_q = request.GET.get("title", "").strip()
    author_q = request.GET.get("author", "").strip()
    category_q = request.GET.get("category", "").strip()

    books = Book.objects.select_related("author", "category", "details").all().order_by("category__name", "title")
    if query:
        books = books.filter(
            Q(title__icontains=query)
            | Q(author__name__icontains=query)
            | Q(category__name__icontains=query)
            | Q(details__isbn__icontains=query)
        )
    else:
        if title_q:
            books = books.filter(title__icontains=title_q)
        if author_q:
            books = books.filter(author__name__icontains=author_q)
        if category_q:
            books = books.filter(category__name__icontains=category_q)

    return render(
        request,
        "book_management/member_books.html",
        {
            "books": books,
            "query": query,
            "title_q": title_q,
            "author_q": author_q,
            "category_q": category_q,
        },
    )


@login_required
def profile(request):
    # This view shows the profile and member borrow history tabs.
    borrowed_records = []
    role = getattr(request.user, "role", "guest")
    is_librarian = request.user.is_staff or request.user.is_superuser or role == "librarian"
    if not is_librarian and role in ["guest", "student"]:
        borrow_status = request.GET.get("borrow_status", "pending").strip().lower()
        base_qs = BorrowRecord.objects.select_related(
            "book", "book__author", "book__category", "book__details", "member"
        ).filter(member__email=request.user.email)

        if borrow_status == "pending":
            borrowed_records = base_qs.filter(status="Pending")
        elif borrow_status == "declined":
            borrowed_records = base_qs.filter(status="Declined")
        elif borrow_status == "accepted":
            borrowed_records = base_qs.filter(status__in=["Accepted", "Active", "Returned", "Overdue"])
        else:
            borrowed_records = base_qs

    return render(request, "book_management/profile.html", {"borrowed_records": borrowed_records})


@login_required
def book_detail(request, book_id):
    # This view shows one book and handles borrow request submission.
    book = get_object_or_404(Book, pk=book_id)
    available_copies = book.available_copies
    today = timezone.localdate()
    max_date = today + timezone.timedelta(days=7)
    current_member = Member.objects.filter(email=request.user.email).first()
    current_phone_number = current_member.phone_number if current_member else ""
    current_full_name = (
        f"{current_member.first_name} {current_member.last_name}".strip()
        if current_member
        else (request.user.get_full_name().strip() or request.user.username)
    )
    current_address = current_member.address if current_member else ""

    error = None
    return_date_str = request.POST.get("return_date", "").strip() if request.method == "POST" else ""
    if request.method == "POST":
        role = getattr(request.user, "role", "guest")
        is_librarian = request.user.is_staff or request.user.is_superuser or role == "librarian"
        if is_librarian or role not in ["guest", "student"]:
            error = "Only guests can submit borrow requests."
        elif available_copies <= 0:
            error = "No copies are available right now."
        else:
            phone_number = request.POST.get("phone_number", "").strip()
            email = request.user.email
            full_name = request.POST.get("full_name", "").strip()
            address = request.POST.get("address", "").strip()

            if not re.fullmatch(r"^\+?\d{10,15}$", phone_number):
                error = "Phone number must be digits only (10-15 digits, optional leading +)."
            elif not full_name:
                error = "Full name is required."
            elif not address:
                error = "Address is required."

            if not error and (not email or not return_date_str):
                error = "Email and return date are required."
            if not error:
                try:
                    return_date = timezone.datetime.strptime(return_date_str, "%Y-%m-%d").date()
                except ValueError:
                    return_date = None

                if not return_date:
                    error = "Invalid return date."
                else:
                    today = timezone.localdate()
                    if return_date < today:
                        error = "Return date must be today or later."
                    elif return_date > today + timezone.timedelta(days=7):
                        error = "You can only borrow for up to one week."
                    else:
                        name_parts = full_name.split()
                        first_name = name_parts[0]
                        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else "Guest"

                        member, _ = Member.objects.get_or_create(
                            email=email,
                            defaults={
                                "first_name": first_name,
                                "last_name": last_name,
                                "phone_number": phone_number,
                                "address": address,
                            },
                        )

                        member.first_name = first_name
                        member.last_name = last_name
                        member.phone_number = phone_number
                        member.address = address
                        member.save()

                        # This check prevents duplicate active or pending requests for the same book.
                        if BorrowRecord.objects.filter(
                            book=book,
                            member=member,
                            status__in=["Pending", "Accepted", "Active"],
                        ).exists():
                            error = "You already have an active request for this book."
                        else:
                            BorrowRecord.objects.create(
                                book=book,
                                member=member,
                                due_date=return_date,
                                status="Pending",
                            )
                            return redirect(f"{reverse('book_management:profile')}?borrow_status=pending")

    return render(
        request,
        "book_management/book_detail.html",
        {
            "book": book,
            "available_copies": available_copies,
            "error": error,
            "today": today,
            "max_date": max_date,
            "current_phone_number": current_phone_number,
            "current_full_name": current_full_name,
            "current_address": current_address,
            "return_date": return_date_str,
        },
    )


@login_required
def edit_profile(request):
    # This view updates the current user's username and profile picture.
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        if not username:
            return render(request, "book_management/edit_profile.html", {"error": "Username cannot be empty."})

        if User.objects.exclude(pk=request.user.pk).filter(username=username).exists():
            return render(request, "book_management/edit_profile.html", {"error": "That username is already taken."})

        request.user.username = username
        profile_pic = request.FILES.get("profile_pic")
        if profile_pic:
            request.user.profile_pic = profile_pic
        request.user.save()
        return redirect("book_management:profile")

    return render(request, "book_management/edit_profile.html")

# This view handles normal guest sign-up without changing the login flow.
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")

        if pass1 != pass2:
            return render(request, "book_management/signup.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "book_management/signup.html", {"error": "Username already taken"})

        User.objects.create_user(username=username, email=email, password=pass1, role="guest")
        return redirect("book_management:login_view") 

    return render(request, "book_management/signup.html")

# This view handles adding a new book record with related details.
@login_required
@librarian_required
def add_book(request):
    authors = Author.objects.all()
    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        author_id = request.POST.get("author")
        category_id = request.POST.get("category")
        isbn_code = request.POST.get("isbn")
        overview = request.POST.get("overview", "").strip()
        pages_raw = request.POST.get("pages", "0").strip()
        total_copies_raw = request.POST.get("total_copies", "1").strip()
        cover_image = request.FILES.get("cover_image")

        try:
            author = get_object_or_404(Author, id=author_id)
            category = get_object_or_404(Category, id=category_id)

            pages = int(pages_raw) if pages_raw.isdigit() else 0
            total_copies = int(total_copies_raw) if total_copies_raw.isdigit() else 1
            
            # This creates the detail record first so it can be linked to the new book.
            details = BookDetails.objects.create(
                isbn=isbn_code,
                overview=overview,
                pages=pages,
                cover_image=cover_image,
            )
            
            Book.objects.create(
                title=title,
                author=author,
                category=category,
                details=details,
                total_copies=total_copies,
            )
            return redirect("book_management:index")

        except IntegrityError:
            # This block shows a user-friendly message when ISBN uniqueness fails.
            return render(request, "book_management/add.html", {
                "authors": authors, 
                "categories": categories, 
                "error": "This ISBN is already in use by another volume!"
            })

    return render(request, "book_management/add.html", {"authors": authors, "categories": categories})

@login_required
@librarian_required
def edit_book(request, book_id):
    # This view loads one book and saves librarian edits.
    book = get_object_or_404(Book, id=book_id)
    authors = Author.objects.all()
    categories = Category.objects.all()

    if request.method == "POST":
        try:
            # This updates base book fields from the submitted form.
            book.title = request.POST.get("title")
            book.author_id = request.POST.get("author")
            book.category_id = request.POST.get("category")

            total_copies_raw = request.POST.get("total_copies", "").strip()
            if total_copies_raw.isdigit():
                book.total_copies = int(total_copies_raw)
            
            # This updates linked book detail fields like ISBN, pages, and cover.
            if hasattr(book, 'details'):
                book.details.isbn = request.POST.get("isbn")
                overview = request.POST.get("overview", "").strip()
                pages_raw = request.POST.get("pages", "").strip()
                if pages_raw.isdigit():
                    book.details.pages = int(pages_raw)
                book.details.overview = overview
                cover_image = request.FILES.get("cover_image")
                if cover_image:
                    book.details.cover_image = cover_image
                # This save can raise IntegrityError if ISBN duplicates another record.
                book.details.save()
            
            book.save()
            return redirect("book_management:index")

        except IntegrityError:
            # This keeps the user on the edit form when ISBN conflicts happen.
            return render(request, "book_management/edit.html", {
                "book": book, 
                "authors": authors, 
                "categories": categories, 
                "error": "This ISBN is already assigned to another volume in the archives!"
            })

    return render(request, "book_management/edit.html", {
        "book": book, "authors": authors, "categories": categories
    })

@login_required
@librarian_required
def delete_book(request, book_id):
    # This view deletes one book and then returns to the catalog.
    # Safety: only allow deletes via POST (prevents accidental deletes via URL visit).
    if request.method != "POST":
        return redirect("book_management:index")

    get_object_or_404(Book, id=book_id).delete()
    return redirect("book_management:index")

@login_required
@librarian_required
def add_author(request):
    # This view adds or deletes authors from the author management page.
    fallback_url = reverse("book_management:add_book")
    next_param = (request.POST.get("next") or request.GET.get("next") or "").strip()
    back_url = (
        next_param
        if next_param
        and url_has_allowed_host_and_scheme(
            url=next_param,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        )
        else fallback_url
    )

    if request.method == "POST":
        # This branch handles deleting an existing author from the dropdown.
        if "delete_author" in request.POST:
            author_id = request.POST.get("author_id")
            if author_id and author_id.isdigit():
                Author.objects.filter(id=int(author_id)).delete()
            return redirect(back_url)

        # This branch handles creating a new author record.
        name = request.POST.get("name", "").strip()
        if name:
            Author.objects.create(name=name)
            return redirect(back_url)

    # This renders the page with the latest author list.
    return render(
        request,
        "book_management/add_author.html",
        {"authors": Author.objects.all(), "back_url": back_url},
    )

@login_required
@librarian_required
def add_category(request):
    # This view adds or deletes categories from the category management page.
    fallback_url = reverse("book_management:add_book")
    next_param = (request.POST.get("next") or request.GET.get("next") or "").strip()
    back_url = (
        next_param
        if next_param
        and url_has_allowed_host_and_scheme(
            url=next_param,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        )
        else fallback_url
    )

    if request.method == "POST":
        if "delete_category" in request.POST:
            category_id = request.POST.get("category_id")
            if category_id and category_id.isdigit():
                Category.objects.filter(id=int(category_id)).delete()
            return redirect(back_url)

        name = request.POST.get("name", "").strip()
        if name:
            Category.objects.create(name=name)
            return redirect(back_url)

    return render(
        request,
        "book_management/add_category.html",
        {"categories": Category.objects.all(), "back_url": back_url},
    )


@login_required
def search_suggestions(request):
    # This view returns quick search suggestions for books, authors, and categories.
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse({"suggestions": []})

    # This keeps suggestion queries lightweight for fast typing feedback.
    max_each = 6
    titles = (
        Book.objects.filter(title__icontains=q)
        .order_by("title")
        .values_list("title", flat=True)[:max_each]
    )
    authors = (
        Author.objects.filter(name__icontains=q)
        .order_by("name")
        .values_list("name", flat=True)[:max_each]
    )
    categories = (
        Category.objects.filter(name__icontains=q)
        .order_by("name")
        .values_list("name", flat=True)[:max_each]
    )

    seen = set()
    suggestions = []
    for label in list(titles) + list(authors) + list(categories):
        if not label:
            continue
        key = label.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        suggestions.append(label)
        if len(suggestions) >= 12:
            break

    return JsonResponse({"suggestions": suggestions})


@login_required
def register_librarian(request):
    # This view allows existing librarians to register a new librarian account.
    # Librarian-only access (head librarian is also a librarian).
    if not getattr(request.user, "is_librarian", False):
        return redirect("book_management:index")

    if request.method == "POST":
        form = LibrarianRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_management:profile")
    else:
        form = LibrarianRegisterForm()

    return render(request, "book_management/librarian_register.html", {"form": form})

def login_view(request):
    # This view handles username/password login for existing users.
    if request.method == "POST":
        u_name = request.POST.get("username")
        p_word = request.POST.get("password")

        # This checks whether the submitted credentials are valid.
        user = authenticate(request, username=u_name, password=p_word)

        if user is not None:
            # This logs in the user using the model backend for CustomUser.
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("book_management:index")
        else:
            # This shows an error message when login credentials do not match.
            return render(request, "book_management/login.html", {"error": "Invalid username or password"})
            
    return render(request, "book_management/login.html")

def logout_user(request):
    # This view logs out the current user and sends them to login.
    logout(request)
    return redirect("book_management:login_view")