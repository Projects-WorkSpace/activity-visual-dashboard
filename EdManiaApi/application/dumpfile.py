"""
    Codes for v1.0

"""

# Views
"""
    Views


class UserChildView(APIView):
    @swagger_auto_schema(
        tags=["Activities"],
        operation_description="This endpoint saves user's children",
        request_body=CreateUserChildSerializer,
        responses=post_mychild_response_schema,
    )
    def post(self, request):
        data = CreateUserChildSerializer(data=request.data)
        if data.is_valid():
            if request.user.is_authenticated:
                child, _ = UserChild.objects.get_or_create(
                    userId=request.user,
                    name=request.data["name"],
                    dateOfBirth=request.data["dateOfBirth"],
                )
                return Response(
                    UserChildSerializer(child, many=False).data,
                    status=status.HTTP_201_CREATED,
                )
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(data.errors, status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=["Activities"],
        operation_description="Get Delivery Managers by emails or All but paginated dicts",
        responses=get_user_children_schema,
    )
    def get(self, request):
        user = request.user
        if user:
            print(user)
            children = UserChild.objects.filter(userId=user)
            print(children)
            return Response(
                UserChildSerializer(children, many=True).data, status=status.HTTP_200_OK
            )

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ChildActivityView(APIView):
    @swagger_auto_schema(
        tags=["Activities"],
        operation_description="This endpoint saves user's children",
        request_body=CreateActivitySerializer,
        responses=post_child_activities_schema,
    )
    def post(self, request):
        data = CreateActivitySerializer(data=request.data)
        if data.is_valid():
            child = UserChild.objects.filter(id=data["userChildId"].value).first()
            if child:
                activity, _ = UserChildActivity.objects.get_or_create(
                    name=data["name"].value, userChildId_id=data["userChildId"].value
                )
                return Response(
                    ChildActivitySerializer(activity, many=False).data,
                    status.HTTP_201_CREATED,
                )
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(data.errors, status.HTTP_400_BAD_REQUEST)

    childId = openapi.Parameter(
        "childId",
        openapi.IN_QUERY,
        description="Get child activities by child Id",
        type=openapi.TYPE_INTEGER,
    )

    @swagger_auto_schema(
        tags=["Activities"],
        operation_description="List child activities",
        manual_parameters=[childId],
        responses=get_child_activities_schema,
    )
    def get(self, request):
        params = request.query_params
        print(params)
        if "childId" in params:
            activities = UserChildActivity.objects.filter(
                userChildId_id=params["childId"]
            )
            return Response(
                ChildActivitySerializer(activities, many=True).data, status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ChildDailyActivityView(APIView):
    @swagger_auto_schema(
        tags=["Activities"],
        operation_description="This endpoint saves child day activities",
        request_body=CreateChildDailyActivitySerializer,
        responses=post_child_daily_activities_schema,
    )
    def post(self, request):
        post_data = request.data.copy()
        data = CreateChildDailyActivitySerializer(data=post_data)
        if data.is_valid():
            recorded_activity = UserChildDailyActivity.objects.filter(
                date=post_data["date"], childActivityId_id=post_data["childActivityId"]
            ).first()
            print(recorded_activity)
            if recorded_activity:
                recorded_activity.points = post_data["points"]
                recorded_activity.hrs = post_data["hrs"]
                recorded_activity.mins = post_data["mins"]
                recorded_activity.save()
                return Response(
                    ChildDailyActivitySerializer(recorded_activity, many=False).data,
                    status.HTTP_201_CREATED,
                )

            else:
                daily_activity = UserChildDailyActivity.objects.create(
                    points=post_data["points"],
                    hrs=post_data["hrs"],
                    mins=post_data["mins"],
                    date=post_data["date"],
                    childActivityId_id=post_data["childActivityId"],
                )
                return Response(
                    ChildDailyActivitySerializer(daily_activity, many=False).data,
                    status.HTTP_201_CREATED,
                )
        return Response(data.errors, status.HTTP_400_BAD_REQUEST)

    childId = openapi.Parameter(
        "childId",
        openapi.IN_QUERY,
        description="Get by day child activities of this child Id",
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
        manual_parameters=[childId, date],
        responses=get_child_daily_activities_schema,
    )
    def get(self, request):
        params = request.query_params
        if "date" in params and "childId" in params:
            day_records = UserChildDailyActivity.objects.filter(
                date=parse_date(params["date"]),
                childActivityId__userChildId_id=params["childId"],
            )
            if day_records:
                return Response(
                    ChildDailyActivitySerializer(day_records, many=True).data,
                    status.HTTP_200_OK,
                )
            else:
                activity = UserChildActivity.objects.filter(
                    userChildId_id=params["childId"]
                )
                return Response(
                    ChildActivitySerializer(activity, many=True).data,
                    status.HTTP_202_ACCEPTED,
                )
        return Response(status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    tags=["Activities"],
    method="post",
    operation_description="This endpoint saves child day activities",
    request_body=CreateChildDailyActivitySerializer(many=True),
    responses=save_all_child_daily_activities_schema,
)
@api_view(["POST"])
def saveMultipleDayActivities(request):
    post_data = request.data.copy()
    data = CreateChildDailyActivitySerializer(data=request.data, many=True)
    if data.is_valid():
        data_list = []
        for x in post_data:
            recorded_activity = UserChildDailyActivity.objects.filter(
                date=x["date"], childActivityId_id=x["childActivityId"]
            ).first()
            if recorded_activity:
                recorded_activity.points = x["points"]
                recorded_activity.hrs = x["hrs"]
                recorded_activity.mins = x["mins"]
                recorded_activity.save()
                data_list.append(recorded_activity)

            else:
                daily_activity = UserChildDailyActivity.objects.create(
                    points=x["points"],
                    hrs=x["hrs"],
                    mins=x["mins"],
                    date=x["date"],
                    childActivityId_id=x["childActivityId"],
                )
                data_list.append(daily_activity)

        return Response(
            ChildDailyActivitySerializer(data_list, many=True).data, status.HTTP_200_OK
        )

    return Response(status.HTTP_400_BAD_REQUEST)


"""

"""
    Models


class UserChild(models.Model):
    name = models.CharField(max_length=100)
    dateOfBirth = models.DateField(null=True, blank=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "User Children"
        verbose_name_plural = "User Children"

    def __str__(self):
        return self.name + " | " + str(self.userId.emailAddress)


class UserChildActivity(models.Model):
    name = models.CharField(max_length=100)
    userChildId = models.ForeignKey(UserChild, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Child Activities"
        verbose_name_plural = "Child Activities"

    def __str__(self):
        return self.name + " | " + str(self.userChildId)


class UserChildDailyActivity(models.Model):
    points = models.IntegerField(default=0)
    hrs = models.IntegerField(default=0)
    mins = models.IntegerField(default=0)
    childActivityId = models.ForeignKey(UserChildActivity, on_delete=models.CASCADE)
    date = models.DateField(default=now)

    class Meta:
        verbose_name = "Daily Child Activities"
        verbose_name_plural = "Daily Child Activities"

    def __str__(self):
        return str(self.date) + " | " + str(self.childActivityId)


class Activities(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Sample Activities"
        verbose_name_plural = "Sample Activities"

    def __str__(self):
        return self.name

"""

"""
    URls

path("mychild", views.UserChildView.as_view(), name="mychild"),
    path("child-activity", views.ChildActivityView.as_view(), name="child_activities"),
    path("day-activity", views.ChildDailyActivityView.as_view(), name="day_activities"),
    path(
        "all-day-activity", views.saveMultipleDayActivities, name="all_day_activities"
    ),

"""


"""
    Admin


@admin.register(UserChild)
class UserChildAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "userId", "dateOfBirth"]


@admin.register(UserChildActivity)
class UserChildActivityAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "userChildId"]


@admin.register(UserChildDailyActivity)
class UserChildDailyActivityAdmin(admin.ModelAdmin):
    list_display = ["id", "points", "hrs", "mins", "childActivityId", "date"]


@admin.register(Activities)
class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]

"""

"""
    Serializers


class UserChildSerializer(serializers.ModelSerializer):
    # user = UserSerializer(source="userId", read_only=True)

    class Meta:
        model = UserChild
        fields = ["id", "name", "dateOfBirth"]


class CreateUserChildSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, min_length=1)
    dateOfBirth = serializers.DateField()


class ChildActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChildActivity
        fields = ["id", "name"]


class CreateActivitySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    userChildId = serializers.IntegerField()


class ChildDailyActivitySerializer(serializers.ModelSerializer):
    childActivity = ChildActivitySerializer(source="childActivityId", read_only=True)

    class Meta:
        model = UserChildDailyActivity
        fields = ["id", "points", "hrs", "mins", "date", "childActivity"]


class CreateChildDailyActivitySerializer(serializers.Serializer):
    points = serializers.IntegerField()
    hrs = serializers.IntegerField()
    mins = serializers.IntegerField()
    date = serializers.DateField()
    childActivityId = serializers.IntegerField()


class NestedActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChildActivity
        fields = [
            "id",
            "name",
            "userChildId",
        ]

"""

"""
    Schemas


get_user_children_schema = {
    200: UserChildSerializer(many=True),
    401: openapi.Response(
        description="Http 400 Error `Bad Request`, Login to access here",
    ),
}

post_mychild_response_schema = {
    200: UserChildSerializer(many=False),
    400: openapi.Response(
        description="Http 400 Error `Bad Request` description",
        examples={"application/json": {"field": ["error message."]}},
    ),
    401: openapi.Response(
        description="Http 401 Error `Unauthorized Request`, Login to access here",
    ),
}

get_child_activities_schema = {
    200: ChildActivitySerializer(many=True),
    400: openapi.Response(
        description="Http 400 Error `Bad Request`, pass the Child Id param",
    ),
}

post_child_activities_schema = {
    200: ChildActivitySerializer(many=False),
    400: openapi.Response(
        description="Http 400 Error `Bad Request` description",
        examples={"application/json": {"field": ["error message."]}},
    ),
}

get_child_daily_activities_schema = {
    200: ChildDailyActivitySerializer(many=True),
    202: ChildActivitySerializer(many=True),
    400: openapi.Response(
        description="Http 400 Error `Bad Request`, pass the Child Id and date parameters",
    ),
}

post_child_daily_activities_schema = {
    200: ChildDailyActivitySerializer(many=False),
    400: openapi.Response(
        description="Http 400 Error `Bad Request`, pass the Child Id and date parameters",
    ),
}

save_all_child_daily_activities_schema = {
    200: ChildDailyActivitySerializer(many=True),
    400: openapi.Response(
        description="Http 400 Error `Bad Request`, Invalid Data",
    ),
}

"""
