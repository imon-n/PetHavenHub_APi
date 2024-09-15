from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Pet_Model, PurchaseHistory, CategoryModel
from .serializers import PetModelSerializer, PurchaseHistorySerializer, CategoryModelSerializer
from transactions.models import Transaction
from transactions.constants import WITHDRAWAL
from rest_framework.permissions import AllowAny

# ViewSet for Pet_Model
class PetModelViewSet(viewsets.ModelViewSet):
    queryset = Pet_Model.objects.all()
    serializer_class = PetModelSerializer
    permission_classes = [AllowAny]  # Ensures only authenticated users can access

    # Action to handle adopting a pet
    @action(detail=True, methods=['post'])
    def adopt_pet(self, request, pk=None):
        pet = get_object_or_404(Pet_Model, pk=pk)
        user_account = request.user.account

        if pet.quantity > 0:
            amount = pet.price
            
            if user_account.balance >= amount:
                user_account.balance -= amount
                user_account.save(update_fields=['balance'])
                
                pet.reduce_quantity()
                
                # Record the purchase history
                PurchaseHistory.objects.create(
                    user=request.user,
                    pet=pet.name,
                    category_name=pet.category_name.category_name,
                    price=pet.price
                )
                
                # Record the transaction
                Transaction.objects.create(
                    account=user_account,
                    amount=amount,
                    balance_after_transaction=user_account.balance,
                    transaction_type=WITHDRAWAL
                )
                
                if pet.quantity == 0:
                    pet.delete()

                return Response({"message": f"You have successfully adopted '{pet.name}'."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Insufficient balance to adopt this pet."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "This pet is out of stock."}, status=status.HTTP_400_BAD_REQUEST)


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = CategoryModel.objects.all()
    serializer_class = CategoryModelSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]


class PurchaseHistoryViewSet(viewsets.ModelViewSet):
    queryset = PurchaseHistory.objects.all() 
    serializer_class = PurchaseHistorySerializer
    permission_classes = [AllowAny]  