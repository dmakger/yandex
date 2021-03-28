from django.db import models
from django.db.models.fields import AutoField


class Courier(models.Model):
    """Класс для работы с курьером"""

    # courier_id = models.AutoField(primary_key=True)
    courier_id = models.IntegerField()
    courier_type = models.CharField(max_length=30)
    enum_type = {
        'foot': 10, 
        'bike': 15, 
        'car': 50
    }
    regions = models.TextField(max_length=469) # Если курьер - сверхчеловек, и развозит на все регионы РФ
    working_hours = models.CharField(max_length=255)
    capacity = models.FloatField(default=0)  # Текущая вместительность
    orders = models.TextField(default='-')  # Все заказы курьера "order_id_1, order_id_2, ..."
    cur_orders = models.CharField(max_length=255, default='-')
    earnings = models.FloatField(default=0)  # Заработок

    def get_as_dict(self):
        """Вернет поля класса в виде словаря"""
        return {
            'courier_id': self.courier_id,
            'courier_type': self.courier_type,
            'regions': self.regions,
            'working_hours': self.working_hours,
            'capacity': self.capacity,
            'orders': self.orders,
            'cur_orders': self.cur_orders,
            'earnings': self.earnings,
        }

    def id_exists(self, pk):
        """Вернет True, если такой courier_id уже существует"""
        try:
            Courier.objects.get(courier_id = pk)
            return True
        except:
            return False

    def get_max_capacity(self):
        """Вернет максимальную грузоподъемность курьера"""
        if self.courier_type == 'foot':
            return 10
        elif self.courier_type == 'bike':
            return 15
        elif self.courier_type == 'car':
            return 50
        return None

    def get_money_for_delivery(self):
        """Вернет денежную сумму за развоз"""
        if self.courier_type == 'foot':
            return 500 * 2
        elif self.courier_type == 'bike':
            return 500 * 5
        elif self.courier_type == 'car':
            return 500 * 9
        return None


    def is_suitable_type(self, courier_t):
        """Вернет True, если такой тип передвижения курьером дозволен"""
        return courier_t in self.enum_type

    def get(self, key):
        """Возвращает значение по ключу (также как и в типе dict)"""
        if key == 'courier_id':
            return self.courier_id
        elif key == 'courier_type':
            return self.courier_type
        elif key == 'regions':
            return self.regions
        elif key == 'working_hours':
            return self.working_hours
        elif key == 'capacity': 
            return self.capacity
        elif key == 'orders': 
            return self.orders
        elif key == 'cur_orders': 
            return self.cur_orders
        elif key == 'earnings': 
            return self.earnings
        return None
    
    def set(self, key, value):
        """Устанавливает значение по ключу (также как и в типе dict)"""
        if key == 'courier_id':
            self.courier_id = value
        elif key == 'courier_type':
            self.courier_type = value
        elif key == 'regions':
            self.regions = value
        elif key == 'working_hours':
            self.working_hours = value
        elif key == 'capacity':
            self.capacity = value
        elif key == 'orders':
            self.orders = value
        elif key == 'cur_orders':
            self.cur_orders = value
        elif key == 'earnings':
            self.earnings = value
            
    def __str__(self):
        return str(self.courier_id)


class Order(models.Model):
    """Класс для работы с заказами"""
    order_id = models.IntegerField()
    weight = models.FloatField()
    region = models.IntegerField()
    delivery_hours = models.CharField(max_length=255)
    assign_time = models.CharField(max_length=30, default='-')
    complete_time = models.CharField(max_length=30, default='-')
    lead_time = models.CharField(max_length=30, default='-')  # Время выполнения заказа 00:00:00.000
    courier = models.IntegerField(default=-1)

    def get_as_dict(self):
        """Вернет поля класса в виде словаря"""
        return {
            'order_id': self.order_id,
            'weight': self.weight,
            'region': self.region,
            'delivery_hours': self.delivery_hours,
            'assign_time': self.assign_time,
            'complete_time': self.complete_time,
            'lead_time': self.lead_time,
            'courier': self.courier,
        }

    def id_exists(self, pk):
        """Вернет True, если такой order_id уже существует"""
        return bool(Order.objects.filter(order_id = pk))

    def get(self, key):
        """Возвращает значение по ключу (также как и в типе dict)"""
        if key == 'order_id':
            return self.order_id
        elif key == 'weight':
            return self.weight
        elif key == 'region':
            return self.region
        elif key == 'delivery_hours':
            return self.delivery_hours
        elif key == 'assign_time':
            return self.assign_time
        elif key == 'complete_time':
            return self.complete_time
        elif key == 'courier':
            return self.courier
        elif key == 'lead_time':
            return self.lead_time
        return None
    
    def set(self, key, value):
        """Устанавливает значение по ключу (также как и в типе dict)"""
        if key == 'order_id':
            self.order_id = value
        elif key == 'weight':
            self.weight = value
        elif key == 'region':
            self.region = value
        elif key == 'delivery_hours':
            self.delivery_hours = value
        elif key == 'assign_time':
            self.assign_time = value
        elif key == 'complete_time':
            self.complete_time = value
        elif key == 'courier':
            self.courier = value
        elif key == 'lead_time':
            self.lead_time = value

    def __str__(self):
        return str(self.order_id)
