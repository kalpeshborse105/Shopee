from django.urls import path
from shopeeapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index', views.index),
    path('about', views.about),
    path('contact', views.contact),
    path('login', views.user_login, name='login'),
    path('register', views.register),
    path('logout', views.user_logout),
    path('addcart/<pid>', views.cart),
    path('laptop_detail/<pid>', views.laptop_detail),
    path('placeorder', views.placeorder),
    path('catfilter/<cv>', views.catfilter),
    path('sort/<sv>', views.sortprice),
    path('pricefilter', views.pricefilter),
    path('viewcart', views.viewcart),
    path('updateqty/<x>/<cid>', views.updateqty),
    path('removecart/<cid>', views.removecart),
    path('removeorder/<cid>', views.removeorder),
    path('fetchorder', views.fetchorderdetails),
    path('makepayment', views.makepayment),
    path('paymentsuccess', views.paymentsuccess),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('orderhistory/<int:cid>/', views.Orderhistory),
    path('update/', views.update,name='update'),
    path('invoice/download/<int:order_id>/', views.invoice_download, name='invoice_download'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
