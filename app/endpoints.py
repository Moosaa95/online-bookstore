from rest_framework import viewsets, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
# from rest_framework.authentication import BaseAuthentication


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


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Token authentication successful
            refresh_token = response.data["refresh"]
            print("VIEW REFRESH", response.data)
            print(refresh_token)
            response.set_cookie("refresh_token", refresh_token, samesite="None")
            request.session["refresh_token"] = refresh_token
            # user = self
            # print('ccheck user access', user, dir(user))
            response.data["message"] = "Login successful"
        else:
            # Token authentication failed
            response.data["message"] = "Invalid credentials"
        return response


class DashboardViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        author_count = Author.objects.count()
        book_count = Book.objects.count()
        category_count = Category.objects.count()

        data = {
            'author_count': author_count,
            'book_count': book_count,
            'category_count': category_count,
        }

        return Response(data)
    

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    