
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
from transactions.constants import DEPOSIT, WITHDRAWAL
from django.shortcuts import get_object_or_404

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]

    MIN_DEPOSIT_AMOUNT = 500  
    MIN_WITHDRAWAL_AMOUNT = 500  

    def perform_create(self, serializer):
        account = self.request.user.account
        transaction_type = serializer.validated_data['transaction_type']
        amount = serializer.validated_data['amount']

        if transaction_type == DEPOSIT:
            if amount < self.MIN_DEPOSIT_AMOUNT:
                return Response(f"Deposit amount must be at least {self.MIN_DEPOSIT_AMOUNT}.")
            account.balance += amount

        elif transaction_type == WITHDRAWAL:
            if amount < self.MIN_WITHDRAWAL_AMOUNT:
                return Response(f"Withdrawal amount must be at least {self.MIN_WITHDRAWAL_AMOUNT}")
            if account.balance < amount:
                return Response("Insufficient balance for withdrawal.")
            account.balance -= amount

        account.save(update_fields=['balance'])
        serializer.save(account=account, balance_after_transaction=account.balance)
