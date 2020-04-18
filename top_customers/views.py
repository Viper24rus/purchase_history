from .models import Customer
from .serializers import CustomerSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser


class CustomerList(APIView):

    def get(self, request):
        list = Customer.objects.all().order_by('-spent_money')[:5]
        for cur in list:
            '''
            поиск товаров из списка покупок каждого покупателя,
            которые купил еще хотя бы один покупатель из списка
            '''
            proc_list = ''
            for item in cur.gems.split(','):
                for temp in list:
                    if cur == temp:
                        continue
                    else:
                        if temp.gems.find(item) != -1:
                            if proc_list == '':
                                proc_list = item
                            else:
                                proc_list = proc_list + ',' + item
            cur.gems = proc_list
        serializer = CustomerSerializer(list, many=True)
        return Response({'response': serializer.data})

    parser_classes = (FileUploadParser, )

    def post(self, request, format='csv'):
        flag = False
        if 'file' not in request.data:
            return Response('Status: Error, Desc: Empty content', status=400)

        file = request.data['file'].open()
        for string in file:
            current_str = [str(b) for b in string.decode().split(',')]
        Customer.objects.all().delete()

        for string in file:
            current_str = [str(b) for b in string.decode().split(',')]

            if current_str == ['\r\n']:
                if flag:
                    flag = False
                else:
                    flag = True

            if flag and current_str != ['\r\n']:
                try:
                    current_customer = Customer.objects.get(username=current_str[0])
                except Customer.DoesNotExist:
                    current_customer = Customer()
                    current_customer.username = current_str[0]
                    current_customer.save()
                current_customer.add_item(current_str[1])
                current_customer.spent_money += int(current_str[2])
                current_customer.save()

        return Response("Status: OK", status=200)
