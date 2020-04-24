from .models import Customer
from .serializers import CustomerSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser

import pdb


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

    def post(self, request, filename, format=None):
        flag = False
        customer_dict = dict()

        if 'file' not in request.data:
            return Response('Status: Error, Desc: Empty content', status=400)

        file = request.data['file'].open()
        
        Customer.objects.all().delete()        

        for string in file:
            current_str = [str(b) for b in string.decode().split(',')]

            if current_str == ['\r\n']:
                if flag:
                    flag = False
                else:
                    flag = True
            
            if flag and current_str != ['\r\n'] and current_str[2].isdigit():
                if not current_str[0] in customer_dict:
                    customer_dict[current_str[0]] = [set(), int(current_str[2])]
                    customer_dict[current_str[0]][0].add(current_str[1])
                else:
                    customer_dict[current_str[0]][0].add(current_str[1])
                    customer_dict[current_str[0]][1] += int(current_str[2])

        for key, value in customer_dict.items():
            
            current_customer = Customer()
            current_customer.username = key
            current_customer.save()
            current_customer.gems = (','.join(str(s) for s in customer_dict[key][0]))
            current_customer.spent_money = customer_dict[key][1]
            current_customer.save()
            
        return Response("Status: OK", status=200)
