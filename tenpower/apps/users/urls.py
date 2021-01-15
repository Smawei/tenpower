from django.urls import path
from apps.users.views import SmsCodeView, RegisteredAPIVieW, LoginAPIView

urlpatterns = [
    # 短信验证码
    path('sms_codes/<mobile>/', SmsCodeView.as_view()),
    # 注册
    path('users/', RegisteredAPIVieW.as_view()),
    # 登录
    path('authorizations/', LoginAPIView.as_view()),
    # path('user/', UserAPIView.as_view()),
]
