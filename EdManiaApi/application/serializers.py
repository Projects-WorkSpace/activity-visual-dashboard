from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from rest_framework.authtoken.models import Token

from .models import UserChild, ChildActivity, ChildDayActivity, Activities


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    Authorization = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["emailAddress", "Authorization"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            emailAddress=validated_data["emailAddress"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user

    def get_Authorization(self, user):
        return getUserToken(user)


# User JWT header token
def getUserToken(user):
    token, _ = Token.objects.get_or_create(user=user)
    return "Token " + token.key


class UserLoginSerializer(serializers.Serializer):
    emailAddress = serializers.EmailField()
    password = serializers.CharField(min_length=6)


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = ["id", "name"]


class UserChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChild
        fields = ["id", "name", "dateOfBirth"]


class UserChildActivitySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(source="activityID", read_only=True)

    class Meta:
        model = ChildActivity
        fields = ["id", "childID", "enabled", "activity"]


class ChildDayActivitySerializer(serializers.ModelSerializer):
    childActivity = UserChildActivitySerializer(
        source="childActivityID", read_only=True
    )

    class Meta:
        model = ChildDayActivity
        fields = ["id", "points", "hrs", "mins", "date", "childActivity"]


# Models Post Serializers


class PostUserChildSerializer(serializers.Serializer):
    name = serializers.CharField()
    dateOfBirth = serializers.DateField()


class PostChildActivitySerializer(serializers.Serializer):
    childID = serializers.IntegerField()
    activityID = serializers.IntegerField()
    enabled = serializers.BooleanField(default=True)


class PostChildDayActivitySerializer(serializers.Serializer):
    childID = serializers.IntegerField()
    activityID = serializers.IntegerField()
    points = serializers.IntegerField()
    hrs = serializers.IntegerField()
    mins = serializers.IntegerField()
    date = serializers.DateField()


class DeleteChildActivitySerializer(serializers.Serializer):
    childActivityID = serializers.IntegerField()
