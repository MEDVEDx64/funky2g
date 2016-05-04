from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=32)
    balance = models.FloatField()
    hide_sold = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username + ': ' \
            + self.nickname + ', ' \
            + str(self.balance) + ' funks'

class Item(models.Model):
    item_string = models.CharField(max_length=128)
    text = models.CharField(max_length=128)
    price = models.FloatField()
    left = models.IntegerField(default=-1)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        s = self.text + ' (' + self.item_string + '), ' + str(self.price) + 'f'
        if self.left >= 0:
            s += ', ' + str(self.left) + ' left'
        return s

class Transaction(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_tn')
    destination = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_tn')
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
