from django.urls import path
from .views import SignupView, SigninView, ProtectedView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', SigninView.as_view()),
    path('protected/', ProtectedView.as_view()),
]