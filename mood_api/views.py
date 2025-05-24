from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    UserRegistrationSerializer,
    MoodEntrySerializer,
    UserSerializer,
    DefaultMoodSerializer,
)
from .models import MoodEntry, DefaultMood
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
import calendar


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            UserSerializer(user, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED,
        )


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class MoodEntryViewSet(viewsets.ModelViewSet):
    serializer_class = MoodEntrySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        queryset = MoodEntry.objects.filter(user=user)
        month_str = self.request.query_params.get("month")
        year_str = self.request.query_params.get("year")
        if month_str and year_str:
            try:
                month = int(month_str)
                year = int(year_str)
                if not (1 <= month <= 12 and year > 1900):
                    return MoodEntry.objects.none()
                _, num_days = calendar.monthrange(year, month)
                start_date = parse_date(f"{year}-{month:02d}-01")
                end_date = parse_date(f"{year}-{month:02d}-{num_days:02d}")
                if start_date and end_date:
                    queryset = queryset.filter(
                        entry_date__gte=start_date, entry_date__lte=end_date
                    )
                else:
                    return MoodEntry.objects.none()
            except ValueError:
                return MoodEntry.objects.none()
        return queryset.order_by("-entry_date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DefaultListView(generics.ListAPIView):
    queryset = DefaultMood.objects.all().order_by("id")
    serializer_class = DefaultMoodSerializer
    permission_classes = [AllowAny]
