from django.urls import path

from .views import *


urlpatterns = [
    path('login/', LogInView.as_view(), name="login"),
    path('logout/', logout, name="logout"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('thankyou/', SignedView.as_view(), name="signed"),
    path('', ProfileView.as_view(), name="profile"),
]
