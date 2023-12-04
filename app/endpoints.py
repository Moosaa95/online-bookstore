from rest_framework import viewsets, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import CreateCustomUserSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode



class CustomUserViewSet(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateCustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        
        try:
           
            serializer = self.get_serializer(data=request.data)
            
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            
            success_message = "User created successfully."

           
            return Response(
                {"message": success_message, "user_email": user.email},
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            # Handle validation errors
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle other exceptions
            print(str(e), "error")
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ActivateAccount(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)

            if user and default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                # Optionally, you can log in the user after activation.
                # Example: login(request, user)
                return Response({"detail": "Account activated successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({"detail": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)