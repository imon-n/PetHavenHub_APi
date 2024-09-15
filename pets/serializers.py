from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CategoryModel, Pet_Model, PurchaseHistory

class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'

class PetModelSerializer(serializers.ModelSerializer):
    category_name = CategoryModelSerializer() 
    author = serializers.StringRelatedField() 
    class Meta:
        model = Pet_Model
        fields = '__all__'


class PurchaseHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField() 
    class Meta:
        model = PurchaseHistory
        fields = '__all__'
