from base.models import NewUserRegistration
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class NewUserSerializer(ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = NewUserRegistration
        fields = ["name", "user_name", "email" ,"date_of_birth", "password", "confirm_password"]
        extra_kwargs={
            'password':{'write_only': True}
        }
    
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if password != confirm_password :
            raise serializers.ValidationError("Password doesn't match")
        
        return data
    
    def create(self, validate_data):
        return NewUserRegistration.objects.create_user(**validate_data)
