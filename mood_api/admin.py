from django.contrib import admin
from .models import DefaultMood, MoodEntry


@admin.register(DefaultMood)
class DefaultMoodAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "image")
    search_fields = ("name", "description")


@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "mood",
        "entry_date",
        "description",
        "created_at",
        "updated_at",
    )
    list_filter = ("user", "mood", "entry_date")
    search_fields = ("user__username", "mood__name", "description")
    date_hierarchy = "entry_date"
    raw_id_fields = ("user", "mood")  # Útil para muitos usuários/moods
