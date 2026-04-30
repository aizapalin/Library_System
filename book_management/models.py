from django.db import models

# This model stores each author that can be linked to books.
class Author(models.Model):
    name = models.CharField(max_length=100)
    
    # This returns the author name in admin and dropdown displays.
    def __str__(self):
        return self.name

# This model stores the available book categories.
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        # This keeps the plural display label clean in admin views.
        verbose_name_plural = "Categories"

    # This returns the category name in admin and dropdown displays.
    def __str__(self):
        return self.name

# This model stores ISBN and extended details for one book.
class BookDetails(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    # This sets the published date to the creation date by default.
    published_date = models.DateField(auto_now_add=True)
    overview = models.TextField(blank=True, default="")
    pages = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)

# This is the main book model used across the library system.
class Book(models.Model):
    title = models.CharField(max_length=200)
    
    # This links each book to one category and keeps category books grouped.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="books")
    
    # This links each book to one author entry.
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    
    # This links one book to one details record.
    details = models.OneToOneField(BookDetails, on_delete=models.CASCADE)

    # This stores the total number of copies owned by the library.
    total_copies = models.PositiveIntegerField(default=1)

    # This returns the book title in admin and related displays.
    def __str__(self):
        return self.title

    @property
    def available_copies(self):
        # This calculates available copies by subtracting active borrow records.
        out_count = self.borrow_records.filter(status__in=["Pending", "Accepted", "Active", "Overdue"]).count()
        return max(0, self.total_copies - out_count)

