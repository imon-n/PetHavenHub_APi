from django.db import models
from django.contrib.auth.models import User

class CategoryModel(models.Model):
    category_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True)
    def __str__(self):
        return self.category_name

class Pet_Model(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='book_images/')
    category_name = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def reduce_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1
            self.save()

class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, related_name='purchase_history', on_delete=models.CASCADE)
    pet = models.CharField(max_length=50)
    category_name = models.CharField(max_length=50)
    price = models.IntegerField()
    purchased_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car} purchased by {self.user.username} on {self.purchased_on}"