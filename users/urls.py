from django.urls import path

from .views import *
from .api_views import *

urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('signout/', signup_page, name='signup'),
    path('cuserlist/', cuser_list, name='cuserlist'),
    path('cuserview/<str:pk>', cuser_view, name='cuserview'),
    path('cuserupdate/<str:pk>', cuser_update, name='cuserupdate'),
    path('clientlist/', client_list, name='clientlist'),
    path('create/', create_user, name='createuser'),
    # urls for API
    path('apilogin/', MyObtainTokenPairView.as_view(), name='login_api'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('createuserapi/', CreateUserAPI.as_view(), name='createuserapi'),
    path('cuserapi/', CuserAPIList.as_view(), name='cuserapi'),
    path('apilogout/', LogoutView.as_view(), name='logout_api'),
    path('userapi/', UserAPI.as_view(), name='user_api'),
    path('change_password/', ChangePasswordView.as_view(), name='auth_change_password'),
]
