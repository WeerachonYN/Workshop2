from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    # TokenRefreshView,
    TokenVerifyView,
)

#views
from webAPI.views.User import api_root,UserViewSet,GroupViewSet,RegisterApi,TokenRefreshView,TokenObtainPairView
from webAPI.views.Cart import cart_list,cart_edit_delete
from webAPI.views.Category import category_list,category_detail
from webAPI.views.Invoice import invoice_list,invoice_detail,checkouts,void_status
from webAPI.views.Product import product_list,product_detail
from webAPI.views.Comment import CommentViewSet
from webAPI.views.ImageUser import ImageUserViewSet
#viewset Custom
GroupViewSet = GroupViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
ImageUser_list = ImageUserViewSet.as_view({
        'get': 'list'
})
ImageUser_detail = ImageUserViewSet.as_view({
         'get': 'retrieve',
         'patch':'patch'

})
comment_list = CommentViewSet.as_view({
     'get': 'list',
     'post': 'create'
})
comment_detail = CommentViewSet.as_view({
     'get': 'retrieve'
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
    #comment
    path('comment/',comment_list,name="comment-list"),
    path('comment/<int:pk>/',comment_detail,name="comment-detail"),
    #Image User
    path('imageUser/',ImageUser_list,name="imageUser-list"),
    path('imageUser/<int:pk>/',ImageUser_detail,name="imageUser-detail"),
    #auth
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/',RegisterApi.as_view(),name = 'register'),
    #views
        #user
    path('group', GroupViewSet, name='group'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
        #product
    path('product/',product_list.as_view(),name='product-list'),
    path('product/<int:pk>/',product_detail.as_view(),name='product-detail'),
         #product_image
        #category
    path('category/', category_list.as_view(),name='category-list'),
    path('category/<int:pk>/',category_detail.as_view(),name='category-detail'),
        #cart
    path('cart/', cart_list.as_view(),name='cart-list'),
    # path('cart')
    path('cart/<int:pk>/',cart_edit_delete.as_view(),name='cart-detail'),
    # path('cart/<int:cart_id>/',cart_Delete.as_view(),name='cart-delete'),
    #invoice
    path('checkout/', checkouts.as_view(),name='checkout'),    
    path('invoice/', invoice_list.as_view(),name='invoice-list'),
    path('invoice/<int:pk>/',invoice_detail.as_view(),name='invoice-detail'),
    #void
    path('invoice/<int:pk>/void/',void_status.as_view(),name='invoice-void'),
        #invoice_item
   
])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)