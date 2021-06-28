from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

#views
from webAPI.views.User import api_root,UserViewSet,GroupViewSet,RegisterApi
from webAPI.views.Cart import cart_list,cart_detail
from webAPI.views.Category import category_list,category_detail
from webAPI.views.Invoice import invoice_list,invoice_detail
from webAPI.views.Invoice_Item import invoice_item_list,invoice_item_detail
from webAPI.views.Product import product_list,product_detail
from webAPI.views.Product_Image import product_Image_list,product_Image_detail

#viewset Custom
GroupViewSet = GroupViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
user_list = UserViewSet.as_view({
    'get': 'list'
})
user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = format_suffix_patterns([

    #api_root & admin
     path('admin/', admin.site.urls),
     path('',api_root),

    #auth
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/',RegisterApi.as_view(),name = 'register'),
    #views
        #user
    path('group', GroupViewSet, name='group'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>', user_detail, name='user-detail'),
        #product
    path('product/',product_list.as_view(),name='product-list'),
    path('product/<int:pk>',product_detail.as_view(),name='product-detail'),
         #product_image
    path('product_image/',product_Image_list.as_view(),name='product_image-list'),
    path('product_image/<int:pk>',product_Image_detail.as_view(),name='product_image-detail'),
        #category
    path('category/', category_list.as_view(),name='category-list'),
    path('category/<int:pk>',category_detail.as_view(),name='category-detail'),
        #cart
    path('cart/', cart_list.as_view(),name='cart-list'),
    path('cart/<int:pk>',cart_detail.as_view(),name='cart-detail'),
         #invoice
    path('invoice/', invoice_list.as_view(),name='invoice-list'),
    path('invoice/<int:pk>',invoice_detail.as_view(),name='invoice-detail'),
        #invoice_item
    path('invoice_item/', invoice_item_list.as_view(),name='invoice_item-list'),
    path('invoice_item/<int:pk>',invoice_item_detail.as_view(),name='invoice_item-detail'),

])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)