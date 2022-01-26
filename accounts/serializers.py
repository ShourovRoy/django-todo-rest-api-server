from rest_framework import serializers
from .models import MyUser



class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = MyUser 
        fields = ['email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        password = validated_data['password']
        user = MyUser.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
        )
        user.set_password(password)
            
        user.save()

        return user
