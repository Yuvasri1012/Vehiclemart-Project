from django.urls import path
from .views import login_page,signup_page,do_login,do_signup,login_view,signup_view

urlpatterns = [
    # HTML
    path('', login_page, name='login'),
    path('signup/', signup_page, name='signup'),

    # 🔥 FORM SUBMIT
    path('do-login/', do_login, name='do_login'),
    path('do-signup/', do_signup, name='do_signup'),

    # 🔥 API
    path('api/login/', login_view, name='login_api'),
    path('api/signup/', signup_view, name='signup_api'),
]