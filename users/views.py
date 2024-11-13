from pprint import pprint

from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, get_user_model
from .models import User, OTP
from .serializers import PhoneNumberSerializer, OTPSerializer, UserProfileSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters
from rest_framework.decorators import permission_classes
from django.urls import reverse
import pdb

def login_page(request):
    return render(request, 'users/login.html')


@permission_classes([AllowAny])
class SendOTPView(APIView):
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user, created = User.objects.get_or_create(phone_number=phone_number)
            otp_code = "12345"
            otp_record = OTP(user=user, code=otp_code)
            otp_record.save()
            return HttpResponseRedirect(reverse('verify-otp') + f'?phone_number={phone_number}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class VerifyOTPView(APIView):
    def get(self, request):
        phone_number = request.GET.get('phone_number')
        return render(request, 'users/verify_otp.html', {'phone_number': phone_number})

    def post(self, request):
        phone_number = request.POST.get('phone_number')
        pprint(request)
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            user = User.objects.filter(phone_number=phone_number).first()
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

            otp_record = OTP.objects.filter(user=user).latest('created_at')
            if otp_record.code != otp:
                error_message = "Invalid OTP, please try again."
                return render(request, 'users/verify_otp.html',
                              {'phone_number': phone_number, 'error_message': error_message})
            login(request, user)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response = HttpResponseRedirect('/users/dashboard/')
            response.set_cookie('access_token', access_token, httponly=True, max_age=10 * 60)
            response.set_cookie('refresh_token', str(refresh), httponly=True, max_age=60 * 60 * 24)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return render(request, 'users/dashboard.html', {'user': user})


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


User = get_user_model()


class UserPagination(PageNumberPagination):
    permission_classes = [IsAuthenticated]
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    serializer_class = UserSerializer
    pagination_class = UserPagination

    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['phone_number', 'username']
    ordering_fields = ['username', 'phone_number']
    ordering = ['username']

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(phone_number__icontains=search) | Q(username__icontains=search)
            )

        return queryset