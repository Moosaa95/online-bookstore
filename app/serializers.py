from django.urls import reverse
from rest_framework import serializers
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .tasks import send_activation_email
from django.conf import settings

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_picture')


class CreateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "password", "first_name", "last_name", "date_of_birth")
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self, validated_data):
        try:
            user = CustomUser.objects.create_user(**validated_data)
            activation_token = self.create_activation_token(user)
            activation_link = self.create_activation_link(user, activation_token)
            activation_url = settings.BASE_URL + activation_link
            html_message = f"""
                        <html>
                            <body>
                                <h2>Activate your account</h2>
                                <p>Thank you for registering. Please click the following link to activate your account:</p>
                                <a href="{activation_url}">{activation_url}</a>
                            </body>
                        </html>""".format(
                context=user, activation_url=activation_url
            )
            self.send_activation_email(user, html_message)
            return user
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def create_activation_token(self, user):
        return default_token_generator.make_token(user)

    def create_activation_link(self, user, activation_token):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        return reverse(
            "activate_account",
            kwargs={"uidb64": str(uid), "token": str(activation_token)},
        )

  
    def send_activation_email(self, user, html_message):
        subject = "Activate Your Account"
        from_email = "moosaabdullahi45@gmail.com"  # Change this to your email address
        recipient_list = user.email
        send_activation_email(
            recipient_list, subject, html_message=html_message, from_email=from_email
        )
