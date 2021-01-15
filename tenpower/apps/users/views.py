from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from utils.jwt import jwt_response_payload_handler
from apps.users.models import User
from django_redis import get_redis_connection
from random import randint
from apps.users.serializers import UserSerializer, LoginJSONWebTokenSerializer


class SmsCodeView(APIView):
    """短信验证码"""
    def get(self, request, mobile):
        try:
            User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            red_cli = get_redis_connection('sms')
            if red_cli.get('flag_%s'%mobile) is not None:
                return Response({'data':{'success':False, 'message':'操作过于频繁'}})
            red_cli.setex('flag_%s'%mobile, 60, 1)
            sms_code = '%04d'% randint(0,9999)
            red_cli.setex(mobile, 300, sms_code)

            return Response({'data':{'success':True, 'message':'ok', 'sms_code':sms_code}})

        else:
            return Response({'data':{'success':False, 'message':'手机号已被注册'}})


class RegisteredAPIVieW(APIView):
    """注册"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        sms = request.data.pop('sms_code')
        redis_cli = get_redis_connection('sms')
        sms_code = redis_cli.get(request.data.get('mobile'))
        if sms_code.decode() != sms:
            return Response({'data':{'success':False, 'message':'验证码错误'}})
        serializer = UserSerializer(data=request.data)
        serializer.is_valid()
        user = serializer.save()
        serializer_jwt = JSONWebTokenSerializer(data=request.data)
        token = serializer_jwt.validate(request.data).get('token')
        data = jwt_response_payload_handler(token, user, request)

        return Response(data)


class LoginAPIView(JSONWebTokenAPIView):
    """登录"""
    serializer_class = LoginJSONWebTokenSerializer


# class UserAPIView(APIView):
#     """用户中心"""
#     authentication_classes = [JSONWebTokenAuthentication]
#
#     def get(self, request):
#         user = request.user
#         serializer = UserSerializer(instance=user)
