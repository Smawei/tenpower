from django.contrib.auth import authenticate
from rest_framework_jwt.serializers import JSONWebTokenSerializer, jwt_payload_handler, jwt_encode_handler
from apps.users.models import User
from rest_framework import serializers
from django.utils.translation import ugettext as _

class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password':{'read_only':True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user

class LoginJSONWebTokenSerializer(JSONWebTokenSerializer):

    def validate(self, attrs):
        credentials = {
            'mobile': attrs.get('mobile'),
            'password': attrs.get('password')
        }
        User.USERNAME_FIELD = 'mobile'
        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)