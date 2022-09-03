from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password_check = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields =("email","password","password_check", "name", "phone", "age", "created_at", "updated_at",)
        read_only_fields = ["created_at", "updated_at"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if data["password"] != data["password_check"]:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        data.pop("password_check") 
        return data

    def save(self, **kwargs):
        user = User.objects.create_user(**self.validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        if not user:
            raise serializers.ValidationError("존재하지 않는 이메일입니다.")
        if not user.check_password(data["password"]):
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data