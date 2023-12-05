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
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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



class TokenObtainPairSerializer(TokenObtainPairSerializer):
    is_first_timer = serializers.SerializerMethodField()

    def get_is_first_timer(self, obj):
        # Retrieve the user from the token and get the is_first_timer value
        user = self.user
        return user.is_first_timer

    @classmethod
    def get_token(cls, user):
        print('poppppp')
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        # token['role'] = user.role
        # token['is_first_timer'] = user.is_first_timer
        # token['verified'] = user.profile.verified
        # token['image'] = str(user.profile.image)

        return token

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'categories', 'description', 'published_date', 'cover_image', 'created_at', 'updated_at', 'created_by']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"