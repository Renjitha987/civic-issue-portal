from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComplaintViewSet, RemarkViewSet
from .web_views import TicketListView


router = DefaultRouter()
router.register(r'complaints', ComplaintViewSet, basename='complaint')
router.register(r'remarks', RemarkViewSet, basename='remark')

urlpatterns = [
    path('list/', TicketListView.as_view(), name='ticket_list'),
    path('', include(router.urls)),
]

