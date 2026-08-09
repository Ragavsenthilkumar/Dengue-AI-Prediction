from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard_home, name='dashboard-home'),
    path('risk-map/', views.risk_map, name='risk-map'),
    path('report/', views.report_breeding_spot, name='report-breeding-spot'),
]
