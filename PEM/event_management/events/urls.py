from django.urls import path 
from .import views 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [ 
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('host_register/', views.host_register, name='host_register'),
    path('host_login/', views.host_login, name='host_login'),
    path('host_logout/', views.host_logout, name='host_logout'),
    path('logout/', views.logout, name='logout'),
    path('music/', views.music, name='music'),
    path('tech/', views.tech, name='tech'),
    path('food/', views.food, name='food'),
    path('fashion/', views.fashion, name='fashion'),
    path('sports/', views.sports, name='sports'),
    path('workshop/', views.workshop, name='workshop'),
    path('events/', views.events, name='events'),
    path('event_detail/<int:id>/', views.event_detail, name='event_detail'),
    path('add_event/', views.add_event, name='add_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('host_profile/', views.host_profile, name='host_profile'),
    path('profile/', views.profile, name='profile'),
    path('profile_pic/', views.profile_pic, name='profile_pic'),
    path('profile_pic/<int:id>/', views.profile_pic, name='profile_pic'),
    path('delete_profile/<int:profile_id>/', views.delete_profile, name='delete_profile'),
    path('checkout/<int:event_id>/', views.checkout, name='checkout'),
    path('event_list/', views.event_list, name='event_list'),
    # path('cart/', views.cart, name='cart'),   
    path('payment/<int:amount>/',views.payment, name='payment'),
    path('success/<int:amount>/<int:id>/<str:payment_id>/<int:session>/',views.success,name="success"),
    path('update_quantity/<int:id>/<str:action>/<str:path>/', views.update_quantity, name='update_quantity'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)