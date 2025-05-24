from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MoodEntry, DefaultMood
from django.contrib.auth.password_validation import (
    validate_password,
)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True, required=True, label="Confirme a senha"
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password2",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "email": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError(
                {"username": "Este usernaame já está em uso."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class DefaultMoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultMood
        fields = ("id", "name", "description", "image")


class MoodEntrySerializer(serializers.ModelSerializer):
    mood_id = serializers.PrimaryKeyRelatedField(
        queryset=DefaultMood.objects.all(),
        source="mood",
        write_only=True,
        label="ID do Humor",
    )
    mood = DefaultMoodSerializer(read_only=True)  # Para exibir detalhes do humor no GET
    user = UserSerializer(read_only=True)

    class Meta:
        model = MoodEntry
        fields = (
            "id",
            "user",
            "mood_id",
            "mood",
            "description",
            "entry_date",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "user",
            "created_at",
            "updated_at",
        )

    def validate_entry_date(self, value):
        request = self.context.get("request")
        user = request.user if request else None

        if (
            self.instance
            and self.instance.entry_date == value
            and self.instance.user == user
        ):
            return value

        if user and MoodEntry.objects.filter(user=user, entry_date=value).exists():
            raise serializers.ValidationError(
                "Já existe uma entrada de humor para esta data."
            )
        return value

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
