from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserAccount
from .serializers import AuthSerializer, LoginSerializer
from django.contrib import messages


# =========================
# 🌐 HTML PAGES
# =========================
def login_page(request):
    return render(request, 'login.html')

def signup_page(request):
    return render(request, 'signup.html')


# =========================
# 🔥 HTML LOGIN (REDIRECT)
# =========================
def do_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = UserAccount.objects.filter(
            username=username,
            password=password
        ).first()

        if not user:
            return redirect('login')

        # ✅ session store
        request.session['user_id'] = user.id
        request.session['role'] = user.role

        return redirect('home')

    return redirect('login')


# =========================
# 🔥 HTML SIGNUP (REDIRECT)
# =========================
def do_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if UserAccount.objects.filter(email=email).exists():
            messages.error(request, "Email already exists ❌")
            return redirect('signup')

        user = UserAccount.objects.create(
            username=username,
            email=email,
            password=password,
            role=role
        )

        # ✅ AUTO LOGIN
        request.session['user_id'] = user.id
        request.session['role'] = user.role

        return redirect('/home/')


# =========================
# 🔥 SIGNUP API (JWT)
# =========================
@api_view(['POST'])
def signup_view(request):
    serializer = AuthSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken()
        refresh['username'] = user.username

        return Response({
            "message": "User created successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================
# 🔥 LOGIN API (JWT)
# =========================
@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = UserAccount.objects.filter(
            username=username,
            password=password
        ).first()

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken()
        refresh['username'] = user.username

        return Response({
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)