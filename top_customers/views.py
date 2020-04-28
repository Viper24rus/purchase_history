from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from .models import Customer, Gem
from .serializers import CustomerSerializer


class CustomerList(APIView):
    parser_classes = (FileUploadParser, )

    def get(self, request):
        top_customers_list = Customer.objects.all().order_by('-spent_money')[:5]

        serializer = CustomerSerializer(top_customers_list, many=True)

        top_gems_list = []

        for cur_gems in serializer.data:
            top_gems_list.extend(cur_gems['gems'])

        for cur_gems in serializer.data:
            cur_gems['gems'] = [x for x in cur_gems['gems']
                                if top_gems_list.count(x) > 1]

        return Response({'response': serializer.data})

    def post(self, request, filename, format=None):
        customer_dict = dict()

        if 'file' not in request.data:
            return Response('Status: Error, Desc: Empty content', status=400)

        uploaded_file = request.data['file'].open()

        Customer.objects.all().delete()
        Gem.objects.all().delete()

        for row in uploaded_file:
            current_row = [str(b) for b in row.decode().split(',')]
            try:
                validate = Customer(username=current_row[0],
                                    spent_money=current_row[2])
                validate.full_clean()

                if current_row[0] in customer_dict:
                    customer_dict[current_row[0]][0].add(current_row[1])
                    customer_dict[current_row[0]][1] += int(current_row[2])
                else:
                    customer_dict[current_row[0]] = [set(),
                                                     int(current_row[2])]
                    customer_dict[current_row[0]][0].add(current_row[1])
                Gem.objects.create(name=current_row[1])

            except:
                continue

        for key, value in customer_dict.items():
            current_customer = Customer()
            current_customer.username = key
            current_customer.spent_money = customer_dict[key][1]
            current_customer.save()
            current_customer.gems.set(customer_dict[key][0])

        return Response("Status: OK", status=200)
