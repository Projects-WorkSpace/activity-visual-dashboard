from drf_yasg import openapi
from .serializers import (
    UserSerializer,
    UserChildSerializer,
    UserChildActivitySerializer,
    ChildDayActivitySerializer,
)

registration_response_schema = {
    200: UserSerializer(many=False),
    400: openapi.Response(
        description="HTTP 400 Error `Bad Request` description",
        examples={"application/json": {"field": ["error message."]}},
    ),
}

login_response_schema = {
    200: UserSerializer(many=False),
    400: openapi.Response(
        description="HTTP 400 Error `Bad Request`",
        examples={"application/json": {"field": ["error message."]}},
    ),
    401: openapi.Response(
        description="HTTP 401 Error description",
        examples={"application/json": {"Error": "You entered the wrong credentials"}},
    ),
    500: openapi.Response(
        description="HTTP 401 Error description",
        examples={
            "application/json": {
                "Error": "User with the following Email does not exist"
            }
        },
    ),
}


get_user_children_schema = {
    200: UserChildSerializer(many=True),
    401: openapi.Response(
        description="HTTP 400 Error `Bad Request`, Login to access here",
    ),
}

post_mychild_response_schema = {
    200: UserChildSerializer(many=False),
    400: openapi.Response(
        description="HTTP 400 Error `Bad Request` description",
        examples={"application/json": {"field": ["error message."]}},
    ),
    401: openapi.Response(
        description="HTTP 401 Error `Unauthorized Request`, Login to access here",
    ),
}

post_child_activity_response_schema = {
    201: UserChildActivitySerializer(many=False),
    400: openapi.Response(
        description="HTTP 400 Error `Bad Request` description",
        examples={"application/json": {"field": ["error message."]}},
    ),
}

get_child_activities_schema = {
    200: UserChildActivitySerializer(many=True),
    400: openapi.Response(description="HTTP 400 Error `Bad Request` description"),
}


get_child_daily_activities_schema = {
    200: ChildDayActivitySerializer(many=True),
    202: UserChildActivitySerializer(many=True),
    400: openapi.Response(
        description="HTTP 400 Error `Bad Request`, pass the Child Id and date parameters",
    ),
}

post_child_day_activities_schema = {
    200: ChildDayActivitySerializer(many=False),
    400: openapi.Response(
        description="HTTP 400 Error `Bad Request`, pass the Child Id and date parameters",
    ),
}

save_all_child_daily_activities_schema = {
    200: ChildDayActivitySerializer(many=True),
    400: openapi.Response(
        description="HTTP 400 Error `Bad Request`, Invalid Data",
    ),
}

post_all_child_activity_response_schema = {
    201: UserChildActivitySerializer(many=True),
    400: openapi.Response(
        description="HTTP 400 Error `Bad Request` description",
        examples={"application/json": {"field": ["error message."]}},
    ),
}

delete_activities_response_schema = {
    200: openapi.Response(
        description="HTTP 200 `Ok` description",
        examples={
            "application/json": {
                "status": ["This child activities were deleted successfuly."]
            }
        },
    ),
    400: openapi.Response(
        description="HTTP 400 Error `Bad Request` description",
        examples={"application/json": {"field": ["error message."]}},
    ),
}

# Reports response Schema


get_reports_child_activity_response_schema = {
    200: openapi.Response(
        description="HTTP 200 Success `OK` description",
        examples={
            "application/json": [
                [
                    {
                        "id": 0,
                        "points": 0,
                        "date": "2023-01-16",
                        "duration": 0,
                        "weekday": "Monday",
                        "activityName": "Reading",
                    }
                ]
            ]
        },
    ),
    400: openapi.Response(
        description="HTTP 400 Error `Bad Request`, Check if correct parameters are passed",
    ),
}
