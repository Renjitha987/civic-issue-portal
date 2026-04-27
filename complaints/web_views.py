from django.db.models import Case, When, Value, IntegerField
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Complaint

class TicketListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Advanced ticket listing view with specific status grouping:
    1. Forwarded
    2. Pending
    3. Resolved
    4. Others
    Maintains LIFO order within each group.
    """
    model = Complaint
    template_name = 'complaints/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 20
    login_url = 'login_page'


    def test_func(self):
        return self.request.user.role == 'ADMIN'

    def get_queryset(self):
        queryset = Complaint.objects.all()
        
        # Filtering by category
        category = self.request.GET.get('category')
        if category and category != 'All':
            queryset = queryset.filter(issue_category=category)
            
        # Custom Status Ordering
        # Order: Forwarded (1), Pending (2), Resolved (3), Others (4)
        queryset = queryset.annotate(
            status_priority=Case(
                When(status='Forwarded', then=Value(1)),
                When(status='Pending', then=Value(2)),
                When(status='Resolved', then=Value(3)),
                default=Value(4),
                output_field=IntegerField(),
            )
        ).order_by('status_priority', '-date_submitted', '-id')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [choice[0] for choice in Complaint.CATEGORY_CHOICES]
        context['selected_category'] = self.request.GET.get('category', 'All')
        return context
