from django.db import models


class Customer(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    gems = models.TextField(default='')
    spent_money = models.IntegerField(default=0)

    def add_item(self, item):
        '''
        метод добавления товара в список товаров,
        которые приобрел покупатель
        '''
        if self.gems.find(item) == -1:
            if self.gems == '':
                self.gems = item
            else:
                self.gems = self.gems + ',' + item

    def __str__(self):
        return self.username
