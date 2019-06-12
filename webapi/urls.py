from django.conf.urls import url, include
from webapi import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)
router.register(r'order', views.OrderViewSet, base_name='order_service')
router.register(r'auth', views.AuthViewSet, base_name='auth_service')

# api url 配置
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^test', views.GetMessageView.as_view()),
]
