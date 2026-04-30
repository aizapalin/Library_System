from django.db import models
from book_management.models import Book
from members.models import Member
from datetime import timedelta, date
from django.conf import settings


class BorrowRecord(models.Model):
    # The ForeignKeys linking App 1 and App 2
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrow_records')
    
    # Date fields required by the rubric
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    
    # Status fields required by the rubric
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
        ('Active', 'Active'),
        ('Returned', 'Returned'),   # Displayed as "Completed" in guest UI
        ('Overdue', 'Overdue'),     # Used for librarian display if you manually set it
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.book.title} borrowed by {self.member.first_name}"

    @property
    def is_overdue(self):
        # A helpful property to check if the book is overdue
        if self.status == "Overdue":
            return True
        if (
            self.status == "Active"
            and self.return_date is None
            and date.today() > self.due_date
        ):
            return True
        return False