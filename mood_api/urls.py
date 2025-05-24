from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, MoodEntryViewSet, DefaultListView
from django.views.decorators.csrf import csrf_exempt

router = DefaultRouter()
router.register(r"moods", MoodEntryViewSet, basename="moodentry")

urlpatterns = [
    path(
        "register/",
        csrf_exempt(UserRegistrationView.as_view()),
        name="user-registration",
    ),
    path("default-moods/", DefaultListView.as_view(), name="default-mood-list"),
    path("", include(router.urls)),
]
