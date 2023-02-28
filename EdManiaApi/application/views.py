from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.dateparse import parse_date
from datetime import timedelta, date
import random

from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    UserChildSerializer,
    UserChildActivitySerializer,
    ChildDayActivitySerializer,
    ActivitySerializer,
    # Post
    PostUserChildSerializer,
    PostChildActivitySerializer,
    PostChildDayActivitySerializer,
    DeleteChildActivitySerializer,
)

from .models import UserChild, ChildActivity, ChildDayActivity, Activities
from .schemas import (
    registration_response_schema,
    login_response_schema,
    get_user_children_schema,
    post_mychild_response_schema,
    post_child_activity_response_schema,
    get_child_activities_schema,
    get_child_daily_activities_schema,
    post_child_day_activities_schema,
    save_all_child_daily_activities_schema,
    post_all_child_activity_response_schema,
    delete_activities_response_schema,
    get_reports_child_activity_response_schema,
)

User = get_user_model()


class UserView(APIView):
    @swagger_auto_schema(
        tags=["Users"],
        operation_description="Creates a new user based on the provided values. If desired an authentication JWT can be generated right away. After creating an account the initial group containing a database is created.",
        request_body=UserSerializer,
        responses=registration_response_schema,
    )
    def post(self, request):
        data = UserSerializer(data=request.data)
        if data.is_valid():
            user = data.create(request.data)

            return Response(UserSerializer(user).data, status.HTTP_201_CREATED)
        else:
            return Response(data.errors, status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    @swagger_auto_schema(
        tags=["Users"],
        operation_description="Authenticates an existing user based on their email and their password. If successful, an access token will be returned.",
        request_body=UserLoginSerializer,
        responses=login_response_schema,
    )
    def post(self, request):
        data = UserLoginSerializer(data=request.data)
        if data.is_valid():
            user = User.objects.filter(
                emailAddress=request.data["emailAddress"]
            ).first()
            if user:
                if user.check_password(request.data["password"]):
                    return Response(
                        UserSerializer(user, many=False).data, status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"Error": "You entered the wrong credentials"},
                        status.HTTP_401_UNAUTHORIZED,
                    )
            else:
                return Response(
                    {"Error": "User with the following Email does not exist"},
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(data.errors, status.HTTP_400_BAD_REQUEST)


class UserChildView(APIView):
    @swagger_auto_schema(
        tags=["Users"],
        operation_description="This endpoint saves user's children",
        request_body=PostUserChildSerializer,
        responses=post_mychild_response_schema,
    )
    def post(self, request):
        data = PostUserChildSerializer(data=request.data)
        if data.is_valid():
            post_data = request.data
            child, _ = UserChild.objects.get_or_create(
                name=post_data["name"],
                dateOfBirth=post_data["dateOfBirth"],
                userID=request.user,
            )
            return Response(
                UserChildSerializer(child, many=False).data, status.HTTP_201_CREATED
            )

        return Response(data.errors, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["Users"],
        operation_description="Get children by User. This endpoint requires `Authorization`",
        responses=get_user_children_schema,
    )
    def get(self, request):
        user = request.user
        if user:
            print(user)
            children = UserChild.objects.filter(userID=user)
            return Response(
                UserChildSerializer(children, many=True).data, status=status.HTTP_200_OK
            )

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ActivityView(APIView):
    @swagger_auto_schema(
        tags=["Activities"],
        operation_description="Get All the activities found in the Database",
        responses={200: ActivitySerializer(many=True)},
    )
    def get(self, request):
        activities = Activities.objects.all()

        return Response(
            ActivitySerializer(activities, many=True).data, status.HTTP_200_OK
        )


class ChildActivityView(APIView):
    @swagger_auto_schema(
        tags=["Activities"],
        operation_description="This endpoint saves child's activity to be recorded",
        request_body=PostChildActivitySerializer,
        responses=post_child_activity_response_schema,
    )
    def post(self, request):
        data = PostChildActivitySerializer(data=request.data)
        if data.is_valid():
            post_data = request.data
            activity, _ = ChildActivity.objects.get_or_create(
                childID_id=post_data["childID"],
                activityID_id=post_data["activityID"],
                enabled=post_data["enabled"],
            )

            return Response(
                UserChildActivitySerializer(activity, many=False).data,
                status.HTTP_201_CREATED,
            )

        return Response(data.errors, status.HTTP_400_BAD_REQUEST)

    childID = openapi.Parameter(
        "childID",
        openapi.IN_QUERY,
        description="Get child activities by child ID",
        type=openapi.TYPE_INTEGER,
    )

    @swagger_auto_schema(
        tags=["Activities"],
        operation_description="List child activities",
        manual_parameters=[childID],
        responses=get_child_activities_schema,
    )
    def get(self, request):
        params = request.query_params
        if "childID" in params:
            activities = ChildActivity.objects.filter(childID_id=params["childID"])
            return Response(
                UserChildActivitySerializer(activities, many=True).data,
                status.HTTP_200_OK,
            )

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ChildDayActivityView(APIView):
    @swagger_auto_schema(
        tags=["Activities"],
        operation_description="This endpoint saves child day activities",
        request_body=PostChildDayActivitySerializer,
        responses=post_child_day_activities_schema,
    )
    def post(self, request):
        data = PostChildDayActivitySerializer(data=request.data)
        if data.is_valid():
            post_data = request.data
            child_activity = ChildActivity.objects.filter(
                childID_id=post_data["childID"], activityID_id=post_data["activityID"]
            ).first()
            if child_activity:
                day_activity = ChildDayActivity.objects.filter(
                    date=post_data["date"], childActivityID_id=child_activity.id
                ).first()
                if day_activity:
                    day_activity.points = post_data["points"]
                    day_activity.hrs = post_data["hrs"]
                    day_activity.mins = post_data["mins"]
                    day_activity.save()
                    return Response(
                        ChildDayActivitySerializer(day_activity, many=False).data,
                        status.HTTP_201_CREATED,
                    )
                else:
                    daily_activity = ChildDayActivity.objects.create(
                        points=post_data["points"],
                        hrs=post_data["hrs"],
                        mins=post_data["mins"],
                        date=post_data["date"],
                        childActivityID_id=child_activity.id,
                    )
                    return Response(
                        ChildDayActivitySerializer(daily_activity, many=False).data,
                        status.HTTP_201_CREATED,
                    )
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data.errors, status.HTTP_400_BAD_REQUEST)

    childID = openapi.Parameter(
        "childID",
        openapi.IN_QUERY,
        description="Search child day activities of this child ID",
        type=openapi.TYPE_INTEGER,
    )
    date = openapi.Parameter(
        "date",
        openapi.IN_QUERY,
        description="Date to record or update day activities",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(
        tags=["Activities"],
        operation_description="List child activities",
        manual_parameters=[childID, date],
        responses=get_child_daily_activities_schema,
    )
    def get(self, request):
        params = request.query_params
        if "date" in params and "childID" in params:
            activities = ChildActivity.objects.filter(childID_id=params["childID"])

            search_recorded_date_activities = []
            for x in activities:
                day_activity = ChildDayActivity.objects.filter(
                    childActivityID_id=x.id, date=params["date"]
                ).first()
                if day_activity:
                    search_recorded_date_activities.append(day_activity)
            if not search_recorded_date_activities:
                return Response(
                    UserChildActivitySerializer(activities, many=True).data,
                    status.HTTP_202_ACCEPTED,
                )
            else:
                activity_list = querySet_to_list(activities)
                recorded_activities = []
                for x in search_recorded_date_activities:
                    recorded_activities.append(x.childActivityID)

                difference = list(set(activity_list) - set(recorded_activities))
                if bool(difference):
                    print("Bool")
                    for x in difference:
                        create_date_activity = ChildDayActivity.objects.create(
                            points=0,
                            hrs=0,
                            mins=0,
                            date=params["date"],
                            childActivityID=x,
                        )
                        search_recorded_date_activities.append(create_date_activity)
                return Response(
                    ChildDayActivitySerializer(
                        search_recorded_date_activities, many=True
                    ).data,
                    status.HTTP_200_OK,
                )
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=["Activities"],
    method="post",
    operation_description="This endpoint takes all child day activity records and saves",
    request_body=PostChildDayActivitySerializer(many=True),
    responses=save_all_child_daily_activities_schema,
)
@api_view(["POST"])
def saveMultipleDayActivities(request):
    data = PostChildDayActivitySerializer(data=request.data, many=True)
    if data.is_valid():
        post_data = request.data.copy()
        data_list = []
        for x in post_data:
            child_activity = ChildActivity.objects.filter(
                childID_id=x["childID"], activityID_id=x["activityID"]
            ).first()
            if child_activity:
                day_activity = ChildDayActivity.objects.filter(
                    date=x["date"], childActivityID_id=child_activity.id
                ).first()
                if day_activity:
                    day_activity.points = x["points"]
                    day_activity.hrs = x["hrs"]
                    day_activity.mins = x["mins"]
                    day_activity.save()
                    data_list.append(day_activity)
                else:
                    daily_activity = ChildDayActivity.objects.create(
                        points=x["points"],
                        hrs=x["hrs"],
                        mins=x["mins"],
                        date=x["date"],
                        childActivityID_id=child_activity.id,
                    )
                    data_list.append(daily_activity)
        return Response(
            ChildDayActivitySerializer(data_list, many=True).data,
            status.HTTP_201_CREATED,
        )
    return Response(status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=["Activities"],
    method="post",
    operation_description="This endpoint saves child's activity to be recorded",
    request_body=PostChildActivitySerializer(many=True),
    responses=post_all_child_activity_response_schema,
)
@api_view(["POST"])
def saveAllNewChildActivities(request):
    data = PostChildActivitySerializer(data=request.data, many=True)

    if data.is_valid():
        post_data = request.data
        saved = []
        for x in post_data:
            activity, _ = ChildActivity.objects.get_or_create(
                childID_id=x["childID"],
                activityID_id=x["activityID"],
                enabled=x["enabled"],
            )
            saved.append(activity)

        return Response(
            UserChildActivitySerializer(saved, many=True).data,
            status.HTTP_201_CREATED,
        )

    return Response(data.errors, status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=["Activities"],
    method="delete",
    operation_description="This endpoint delete child's activities",
    request_body=DeleteChildActivitySerializer(many=True),
    responses=delete_activities_response_schema,
)
@api_view(["DELETE"])
def deleteChildActivitiesView(request):
    data = DeleteChildActivitySerializer(data=request.data, many=True)
    if data.is_valid():
        post_data = request.data
        for x in post_data:
            try:
                activity = ChildActivity.objects.get(id=x["childActivityID"])
                activity.delete()
            except:
                pass
        return Response(
            {"status": "This child activities were deleted successfuly"},
            status.HTTP_200_OK,
        )

    return Response(data.errors, status.HTTP_400_BAD_REQUEST)


# Other functions
def querySet_to_list(qs):
    """
    this will return python list<dict>
    """
    return [q for q in qs]


# Plotting API queries

childID = openapi.Parameter(
    "childID",
    openapi.IN_QUERY,
    description="Request reports of this child ID",
    type=openapi.TYPE_INTEGER,
)
startDate = openapi.Parameter(
    "startDate",
    openapi.IN_QUERY,
    description="The start date for the date range to filter the reports by",
    type=openapi.TYPE_STRING,
)
endDate = openapi.Parameter(
    "endDate",
    openapi.IN_QUERY,
    description="The end date for the date range to filter the reports by",
    type=openapi.TYPE_STRING,
)


@swagger_auto_schema(
    tags=["Reports"],
    method="GET",
    operation_description="Retrieve a list of weekly reports",
    manual_parameters=[childID, startDate, endDate],
    responses=get_reports_child_activity_response_schema,
)
@api_view(["GET"])
def getWeeklyChildActivityRecordsView(request):
    params = request.query_params

    if "childID" in params and "startDate" in params and "endDate" in params:
        child_activities = ChildActivity.objects.filter(childID_id=params["childID"])

        # Evaluate date range to analyze
        start_date = parse_date(params["startDate"])
        end_date = parse_date(params["endDate"])
        days_range = []
        delta = timedelta(days=1)
        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        while start_date <= end_date:
            days_range.append(start_date)
            start_date += delta

        if child_activities:
            activities = []
            for x_date in days_range:
                day_record = []
                for x_activity in child_activities:
                    try:
                        day_activity = ChildDayActivity.objects.get(
                            childActivityID=x_activity, date=x_date
                        )
                        day_record.append(
                            {
                                "id": day_activity.id,
                                "points": day_activity.points,
                                "date": x_date.strftime("%Y-%m-%d"),
                                "duration": (day_activity.hrs * 60) + day_activity.mins,
                                "weekday": days[x_date.weekday()],
                                "activityName": x_activity.activityID.name,
                            }
                        )

                    except:
                        day_record.append(
                            {
                                "id": random.randint(-100, -1),
                                "points": 0,
                                "date": x_date.strftime("%Y-%m-%d"),
                                "duration": 0,
                                "weekday": days[x_date.weekday()],
                                "activityName": x_activity.activityID.name,
                            }
                        )

                activities.append(day_record)
                day_record = []

            return Response(activities, status=status.HTTP_200_OK)

        return Response([], status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
