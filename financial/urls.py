from django.contrib import admin 
from django.urls import path 
from dashboard import views 
  
urlpatterns = [ 
    path('logout/', views.custom_logout, name="logout"), 
    path('pdf/', views.pdf , name='pdf'), 
    path('admin/', admin.site.urls), 
    path('login/' , views.login_page, name='login'), 
    path('register/', views.register_page, name='register'), 
    path('', views.expenses, name='expenses'), 
    path('update_expense/<id>', views.update_expense, name='update_expense'), 
    path('delete_expense/<id>', views.delete_expense, name='delete_expense'), 
    path('salary/', views.salary, name='salary'),
    path('calculate_time/', views.calculate_time, name='calculate_time'),
    path('time_required/', views.time_required, name='time_required'),
]