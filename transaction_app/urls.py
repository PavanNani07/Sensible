from django.urls import path
from .views import TransactionCreateView, TransactionListView, TransactionDetailView, TransactionUpdateView

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/create/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('transactions/<int:pk>/update/', TransactionUpdateView.as_view(), name='transaction-update'),
]
