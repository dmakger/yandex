from rest_framework import exceptions, serializers, status, viewsets
from .serializers import CourierSerializer, OrderSerializer
from .models import Courier, Order
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from django.utils import timezone
import datetime

# class AbstractCourier:


# class AbstractOrder:


class CourierFunctions:
    """
    Класс с функциями помощи модели Courier. 
    В каком-то смысле класс с приватными функциями
    """

    def __init__(self):
        pass

    def id_exists(self, data):
        """Вернет True, если такой id уже существует"""
        type_data = type(data)
        pk = data
        if type_data == dict:
            pk = data['courier_id']
        return bool(Courier.objects.filter(courier_id = pk))

    def all_data_exists(self, data):
        """Если все поля существуют, вернет True"""
        if data.get('courier_id') != None and \
            data.get('courier_type') != None and \
            data.get('regions') != None and \
            data.get('working_hours') != None:
            return True
        return False

    def is_courier_valid(self, data):
        """Проверка валидный ли курьер"""
        # Если тип курьера не подходит
        if data.get('courier_type') != None:
            if data['courier_type'] not in Courier.enum_type:
                return False
        # Если списки оказались пустыми
        if data.get('regions') != None:
            if len(data['regions']) == 0 :
                return False
        # Если список пустой или не правильно введено время
        if data.get('working_hours') != None:
            if len(data['working_hours']) == 0:
                return False
            else:
                working_hours = data['working_hours'][:]
                if type(working_hours) == str:
                    working_hours = working_hours.split(',')
                for time in working_hours:
                    parts = time.split('-')
                    if len(parts) != 2:
                        return False
                    for part in parts:
                        if len(part.split(':')) != 2:
                            return False
        return True

    def get_as_date(self, **data):
        """Меняет строку на объект типа 'datetime' """
        if data.get('format'):
            d = datetime.datetime.strptime(data['date'], data['format'])
        else:
            format_date = '%Y-%m-%dT%H:%M:%S.%fZ'
            d = datetime.datetime.strptime(data['date'], format_date)
        return d

    def get_as_seconds(self, time):
        """Вернет время в секундах"""
        if type(time) == str:
            time = self.get_as_date(date=time, format='%H:%M:%S')
        return time.hour*60*60 + time.minute*60 + time.second


class OrderFunctions:
    """
    Класс с функциями помощи модели Order. 
    В каком-то смысле класс с приватными функциями
    """

    def __init__(self):
        pass

    def id_exists(self, data):
        """Вернет True, если такой id уже существует"""
        type_data = type(data)
        pk = data
        if type_data == dict:
            pk = data['order_id']
        return bool(Order.objects.filter(order_id = pk))

    def all_data_exists(self, data):
        """Если все поля существуют, вернет True"""
        if data.get('order_id') != None and \
            data.get('weight') != None and \
            data.get('region') != None and \
            data.get('delivery_hours') != None:
            return True
        return False

    def is_order_valid(self, data):
        """Валиден ли заказ"""
        # Если вес > 50 и вес < 0.01        
        if data.get('weight') != None:
            if (data['weight'] > 50) or (data['weight'] < 0.01):
                return False
        # Если списки оказались пустыми
        if data.get('working_hours') != None:
            if len(data['working_hours']) == 0:
                return False
        return True

    def suitable_in_time(self, courier_hours, delivery_hours):
        """Вернет True, если время подходит"""
        # Разбиваем на списки: '11:35-14:05,09:00-11:00' ==> ['09:00-11:00', '11:35-14:05']
        courier_hours = sorted(courier_hours.split(','))
        delivery_hours = sorted(delivery_hours.split(','))

        for courier_h in courier_hours:
            courier_h = sorted(courier_h.split('-'))  # 11:00-09:00 ==> ['09:00', '11:00']
            for delivery_h in delivery_hours:
                delivery_h = sorted(delivery_h.split('-'))
                # Находим пересечение времени. (подходит ли время)
                if (courier_h[0] <= delivery_h[0] and courier_h[1] >= delivery_h[0]) or\
                    (courier_h[0] >= delivery_h[0] and courier_h[0] <= delivery_h[1]):
                    return True
        return False

    def is_order_suitable(self, order, courier, max_capacity):
        """
        Вернет True, если заказ подходит курьеру.
        Учитывет следующие факторы:
            1. Заказ в регионе курьера
            2. Заказ можно доставить в рабочее время курьера
            3. У курьера хватает места для заказа
        """
        return str(order.region) in courier['regions'] and\
            self.suitable_in_time(courier['working_hours'], order.delivery_hours) and\
            courier['capacity'] + order.weight <= max_capacity

    def get_datetime_today(self):
        """Возвращает сегодняшнюю дату в таком виде: 2021-03-28T13:32:08Z"""
        return str(datetime.datetime.utcnow().replace().isoformat())[:-4] + 'Z'

    def get_as_date(self, date):
        """Меняет строку на объект типа 'datetime' """
        format_date = '%Y-%m-%dT%H:%M:%S.%fZ'
        d = datetime.datetime.strptime(date, format_date)
        print(d)
        return d

    def get_time_difference(self, date1, date2):
        """Вернет разницу между датами"""
        if type(date1) == str:
            date1 = self.get_as_date(date1)
        if type(date2) == str:
            date2 = self.get_as_date(date2)
        return date1 - date2



class CourierView(generics.GenericAPIView):
    """Вьюшка для работы с курьером"""

    permission_classes = [permissions.AllowAny]
    serializer_class = CourierSerializer

    def post(self, request):
        """ЗАПРОС - POST. Добавляем в бд новых курьеров"""
        print('----------')
        print('Добавление в бд новых курьеров')
        valid_id = list()  #Валидные курьеры
        no_valid_id = list()  #Не валидные курьеры
        courier_help = CourierFunctions()  # Объект класса с функциями помощи
        # Составляем списки валидных и безвалидных курьеров
        for data in request.data['data']:
            # Если какое-то поле не ввели
            if not courier_help.all_data_exists(data):
                no_valid_id.append({"id": data['courier_id']})
                continue
            # Переформировываем списки в строки
            data['regions'] = ','.join([str(region) for region in data['regions']])
            data['working_hours'] = ','.join(data['working_hours'])

            # Проверки на валидных и невалидных
            data_valid = courier_help.is_courier_valid(data) and not courier_help.id_exists(data) #Устраивают ли данные
            if data_valid:
                serializer = CourierSerializer(data=data)
            # Сохраним данные
            if data_valid and serializer.is_valid(raise_exception=True):
                valid_id.append({"id": data['courier_id']})
                serializer.save()
            else:
                no_valid_id.append({"id": data['courier_id']})

        print("valid_id: ", valid_id)
        print("no_valid_id: ", no_valid_id)

        # Если есть не валидные курьеры. Вернем исключение 400
        if no_valid_id:
            raise exceptions.ParseError(detail={
                "validation_error": {
                    'couriers': no_valid_id
                }
            })
        return Response({
            'couriers': valid_id,
        })

    def patch(self, request, courier_id):
        """ЗАПРОС - PATCH. Обновляем данные в бд по курьеру"""
        print('----------')
        print('Обновляение данных курьера в бд')
        result = request.data
        courier_help = CourierFunctions()  # Объект класса с функциями помощи
        # Проверяем что данные правельны
        if not courier_help.is_courier_valid(result):
            raise exceptions.ParseError()
        try:
            courier = Courier.objects.get(courier_id=courier_id)
            answer = {
                "courier_id": courier.courier_id,
                "courier_type": courier.courier_type,
                "regions": courier.regions,
                "working_hours": courier.working_hours,
            }
        except:
            raise exceptions.ParseError()
        for key in result:
            if courier.get(key):
                new_value = result[key]
                if type(result[key]) == list:
                    new_value = ','.join([str(part) for part in result[key]])
                answer[key] = new_value

        serializer = CourierSerializer(data=answer)
        serializer.is_valid(raise_exception=True)
        serializer.update(courier, answer)
        return Response(answer)

    def get(self, request, courier_id):
        print()
        print("---------")
        print("courier_id: ", courier_id)
        try:
            courier = Courier.objects.get(courier_id=courier_id)
            if courier.orders == '-':
                return Response({
                    "courier_id": courier.courier_id, 
                    "courier_type": courier.courier_type, 
                    "regions": courier.regions, 
                    "working_hours": courier.working_hours, 
                    "earnings": courier.earnings, 
                })
        except:
            raise exceptions.ParseError()

        orders = Order.objects.filter(courier=courier_id)
        dict_regions = dict()  # Словарь регонов: {region1: [region_lead_time1, ...], ...}
        # Формируем dict_regions
        courier_help = CourierFunctions()  # Объект класса с функциями помощи
        for order in orders:
            lead_time = courier_help.get_as_seconds(order.lead_time)
            if order.region not in dict_regions:
                dict_regions[order.region] = [lead_time]
            else:
                dict_regions[order.region].append(lead_time)

        t = min([sum(dict_regions[key])/len(dict_regions[key]) for key in dict_regions])
        rating = round((3600 - min(t, 3600))/3600 * 5, 2)

        return Response({
            "courier_id": courier.courier_id, 
            "courier_type": courier.courier_type, 
            "regions": courier.regions, 
            "working_hours": courier.working_hours, 
            "rating": rating,
            "earnings": courier.earnings, 
        })


class OrderView(generics.GenericAPIView):
    """Вьюшка для работы с заказами"""
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderSerializer
    
    def post(self, request):
        """ЗАПРОС - POST. Добавляем в бд новый заказ"""
        print('----------')
        valid_id = list()  #Валидные курьеры
        no_valid_id = list()  #Не валидные курьеры
        order_help = OrderFunctions()  # Объект класса с функциями помощи
        # Составляем списки валидных и безвалидных курьеров
        for data in request.data['data']:
            if not order_help.all_data_exists(data):
                no_valid_id.append({"id": data['order_id']})
                continue
            # Переформировываем списки в строки
            data['delivery_hours'] = ','.join(data['delivery_hours'])
            # Проверки на валидных и невалидных
            data_valid = order_help.is_order_valid(data) and not order_help.id_exists(data)  #Устраивают ли данные
            if data_valid:
                serializer = OrderSerializer(data=data)
            # Сохраним данные
            if data_valid and serializer.is_valid(raise_exception=True):
                valid_id.append({"id": data['order_id']})
                serializer.save()
            else:
                no_valid_id.append({"id": data['order_id']})

        # Если есть не валидные курьеры. Вернем исключение 400
        if no_valid_id:
            raise exceptions.ParseError(detail={
                "validation_error": {
                    'orders': no_valid_id
                }
            })
        # Вернем все валидные courier_id
        return Response({
            'orders': valid_id,
        })


class OrderAssignView(generics.GenericAPIView):
    """Вьюшка для работы с заказами"""
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderSerializer

    def post(self, request):
        """ЗАПРОС - POST. Назначает курьеру заказы, и возращает заказы которые назначил"""
        print()
        print("=== OrderAssignView ===")

        try:
            courier = Courier.objects.get(courier_id=request.data['courier_id'])
        except:
            raise exceptions.ParseError()

        print("courier: ", courier.get_as_dict())
        order_help = OrderFunctions()  # Объект с функциями помощи для модели Order
        # У курьера ещё нет заказов
        if courier.cur_orders == '-':
            assign_time = order_help.get_datetime_today()  # Сегодняшняя дата
            # заказы = Получем отсортированный по весу список объектов, из свободных заказов
            orders = sorted(Order.objects.filter(assign_time = '-'), key = lambda x: x.weight)
            assigned_orders = list()  # назначенные заказы: [{'id': order_id}, ...]
            updated_courier = courier.get_as_dict()  # Курьер в виде словаря
            # Максимальная нагрузка курьера
            max_capacity = courier.get_max_capacity()
            # Если у курьера ещё осталось место
            if courier.capacity <= max_capacity:
                for order in orders:
                    # Подходит ли курьеру
                    if order_help.is_order_suitable(order, updated_courier, max_capacity):    
                        print('order: ', order.get_as_dict())
                        updated_courier['capacity'] += order.weight  # Добавим вес_заказа курьеру
                        assigned_orders.append({
                            'id': order.order_id
                        })
                        # Добавляем курьеру заказ
                        # updated_courier['orders'] += f",{order.order_id}:{order.region}:x"  
                        updated_courier['cur_orders'] += ',' + str(order.order_id)
                        # Обновляем данные заказа
                        order_dict = order.get_as_dict()
                        order_dict['assign_time'] = assign_time  # Устанавливаем дату_назначения
                        order_dict['courier'] = courier.courier_id  # Устанавливаем курьера к заказу
                        serializer = OrderSerializer(data = order_dict)  
                        serializer.is_valid(raise_exception = True)
                        serializer.update(order, order_dict)
            
            # Если курьеру выдали заказы
            if assigned_orders:
                updated_courier['cur_orders'] = updated_courier['cur_orders'][2:]
                if updated_courier['orders'] == '-':
                    updated_courier['orders'] = updated_courier['cur_orders']
                else:
                    updated_courier['orders'] += ',' + updated_courier['cur_orders']
                # Обновляем (бд) таблицу курьера
                serializer = CourierSerializer(data = updated_courier)
                serializer.is_valid(raise_exception = True)
                serializer.update(courier, updated_courier)
        # У курьера уже есть заказы
        else:
            # Формируем список назначенных заказов к курьеру. [{'id': order_id}, ...]
            # assigned_orders = [{'id': order.courier} for order in Order.objects.filter(courier = courier.courier_id)]
            assigned_orders = list()
            for order in Order.objects.filter(courier = courier.courier_id):
                assigned_orders.append({'id': order.order_id})
            # Дата назначения заказов курьеру
            assign_time = Order.objects.filter(order_id = assigned_orders[0]['id'])[0].assign_time

        # Если нет свободных заказов, вернет пустой список orders
        if not assigned_orders:
            return Response({
                'orders': assigned_orders,
            })

        return Response({
            'orders': assigned_orders,
            'assign_time': assign_time,
        })


class OrderCompleteView(generics.GenericAPIView):
    """Вьюшка для работы с заказами"""
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderSerializer

    def post(self, request):
        """ЗАПРОС - POST. Устанавливает выполнение заказа"""
        print()
        print("=== OrderCompleteView ===")

        print(request.data)
        try:
            courier = Courier.objects.get(courier_id=request.data['courier_id'])
            order = Order.objects.get(order_id=request.data['order_id'])
            complete_time = request.data['complete_time']
        except:
            raise exceptions.ParseError()

        if (order.courier == courier.courier_id) and (order.assign_time != '-'):
            if order.complete_time != '-':
                return Response({
                    'order_id': order.order_id,
                })
            order_help = OrderFunctions()  # Объект с функциями помощи для модели Order
            update_order = order.get_as_dict()
            update_order['complete_time'] = complete_time  # Устанавливаем время завершения
            # Время выполнения заказа
            update_order['lead_time'] = \
                str(order_help.get_time_difference(complete_time, update_order['assign_time']))

            serializer = OrderSerializer(data = update_order)  
            serializer.is_valid(raise_exception = True)
            serializer.update(order, update_order)
        else:
            raise exceptions.ParseError()
        
        update_courier = courier.get_as_dict()  # Данные о курьере в виде словаря (его будем изменять)
        update_courier['capacity'] -= order.weight  # Отнимаем вес из объема
        if update_courier['capacity'] < 0:
            update_courier['capacity'] = 0
        # Убираем из списка текущих заказов
        update_courier['cur_orders'] = ','.join(update_courier['cur_orders'].split(',')[:-1])
        # Если список текущих заказов пуст, то прибавляем новую сумму к деньгам курьера
        if len(update_courier['cur_orders']) == 0:
            update_courier['earnings'] += courier.get_money_for_delivery()
            update_courier['cur_orders'] = '-'
        # Обновляем данные
        serializer = CourierSerializer(data = update_courier)  
        serializer.is_valid(raise_exception = True)
        serializer.update(courier, update_courier)
        
        return Response({
            'order_id': order.order_id,
        })
