from django.urls import path
from users.views import LoginView, Logout, CreateUser, LandingPage

app_name = "users"


urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("create-account", CreateUser.as_view(), name="create_user"),
    path("logout", Logout, name="logout"),
    path("home", LandingPage.as_view(), name="landing"),

]