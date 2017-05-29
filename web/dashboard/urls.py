from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard_page, name='dashboard_page'),
    url(r'^predict/', views.predict_data, name='predict_data'),
]
