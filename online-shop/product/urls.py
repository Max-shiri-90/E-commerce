from django.urls import path, re_path
from . import views


app_name = "product"

urlpatterns = [
    path('', views.ProductListView.as_view(), name="product-list"),
    path('special/', views.SpecialListView.as_view(), name="special-list"),
    re_path(r'^product/(?P<slug>[-\w]+)/(?P<pk>\d+)/$', views.ProductDetailView.as_view(), \
            name="product-detail"),
    re_path(r'^like/(?P<slug>[-\w]+)/(?P<pk>\d+)/$', views.like, name="like"),
    path('like-list/', views.LikeListView.as_view(), name="like-list"),
]