from rest_framework import pagination
from rest_framework.response import Response
from webAPI.models.Invoice import invoice
class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param ='page_size'
    max_page_size = 10
    page_query_param = 'page'
   
class CustomPaginations(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param ='page_size'
    max_page_size = 10
    page_query_param = 'page'
    def get_paginated_response(self, data):
        wait = invoice.objects.filter(user=self.request.user,status='Wait')
        success = invoice.objects.filter(user=self.request.user,status='Success')
        cancel = invoice.objects.filter(user=self.request.user,status='Cancel')
        status_all  = invoice.objects.filter(user=self.request.user)
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'status':{'wait': wait.count(),
            'success':success.count(),
            'cancel':cancel.count(),
            'all':status_all.count(),
            },
           
            
            'results': data
        })