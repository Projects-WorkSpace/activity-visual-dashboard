from django.urls import path
from . import views

urlpatterns = [
    path("register", views.UserView.as_view(), name="register_user"),
    path("login", views.UserLoginView.as_view(), name="login_user"),
    path("mychild", views.UserChildView.as_view(), name="mychild"),
    path("activity", views.ActivityView.as_view(), name="activities"),
    path("child-activity", views.ChildActivityView.as_view(), name="child_activities"),
    path("day-activity", views.ChildDayActivityView.as_view(), name="day_activities"),
    path(
        "post-all-day-activity",
        views.saveMultipleDayActivities,
        name="all_day_activities",
    ),
    path(
        "post-all-child-activity",
        views.saveAllNewChildActivities,
        name="all_child_activities",
    ),
    path(
        "delete-child-activities",
        views.deleteChildActivitiesView,
        name="all_child_activities",
    ),
    path(
        "reports-weekly",
        views.getWeeklyChildActivityRecordsView,
        name="weekly_reports",
    ),
]
