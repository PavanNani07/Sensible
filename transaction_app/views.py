from rest_framework import generics
from .models import Transaction
from .serializers import TransactionSerializer, TransactionStatusUpdateSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status  # Used to return HTTP status codes

class TransactionCreateView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        # Set the default status for new transactions to "PENDING"
        serializer.save(status='PENDING')

    # No need to override `create()` method unless you need custom behavior
    # DRF will handle the default behavior automatically

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        # Fetch the user_id from the query parameters and filter transactions accordingly
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            return Transaction.objects.filter(user_id=user_id)
        return Transaction.objects.all()

class TransactionDetailView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

# TransactionUpdateView is generally fine, but I'll make it clearer.
class TransactionUpdateView(generics.UpdateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionStatusUpdateSerializer

    # DRF will automatically handle object retrieval based on the primary key (`pk`),
    # so the `update()` method is optional unless you have specific behavior to add.

    def update(self, request, *args, **kwargs):
        # Retrieve the transaction object by `pk` (transaction_id)
        transaction = get_object_or_404(Transaction, pk=kwargs['pk'])

        # Get the status from the request data
        status_value = request.data.get('status')

        # Validate the status
        if status_value and status_value in ['COMPLETED', 'FAILED']:
            # Update the status and save
            transaction.status = status_value
            transaction.save()

            # Return the updated transaction data with a 200 OK status
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_200_OK)

        # If the status is invalid, return an error response
        return Response(
            {"detail": "Invalid status value. Must be 'COMPLETED' or 'FAILED'."},
            status=status.HTTP_400_BAD_REQUEST
        )
