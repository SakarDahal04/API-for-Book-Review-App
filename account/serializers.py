from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from account.models import User
from django.contrib.auth.password_validation import validate_password

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="User with this email already exists"
            )
        ]
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'confirm_password')

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError(
                {"messsage": "Password and Confirm Password doesn't match"}
            )
            
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'email', 'username']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old Password in incorrect")
        return value

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'message': 'Passwords do not match'})
        validate_password(attrs['new_password'], self.context['request'].user)
        return attrs
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user