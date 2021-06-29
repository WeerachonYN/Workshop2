from rest_framework.filters import OrderingFilter

class MyCustomOrdering(OrderingFilter):

    allowed_custom_filters = ['price']
    # fields_related = {
    #     'user_city': 'user__city__name', # ForeignKey Field lookup for ordering
    #     'user_country': 'user__country__name'
    # }
    def get_ordering(self, request, queryset, view):
        params = request.query_params.get(self.ordering_param)
        print('hellow world')