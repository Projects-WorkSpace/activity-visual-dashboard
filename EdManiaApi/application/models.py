from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now


class UserManager(BaseUserManager):
    def create_user(self, emailAddress, password=None):
        if not emailAddress:
            raise ValueError("You must enter Email Address")

        user = self.model(emailAddress=emailAddress)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, emailAddress, password=None):
        user = self.create_user(emailAddress, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    emailAddress = models.EmailField(unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "emailAddress"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"

    def __str__(self) -> str:
        return self.emailAddress

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class UserChild(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dateOfBirth = models.DateField()

    class Meta:
        verbose_name = "User Children"
        verbose_name_plural = "User Children"

    def __str__(self):
        return self.name + " | " + str(self.userID.emailAddress)


class Activities(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Activities"
        verbose_name_plural = "Activities"

    def __str__(self):
        return self.name


class ChildActivity(models.Model):
    childID = models.ForeignKey(UserChild, on_delete=models.CASCADE)
    activityID = models.ForeignKey(Activities, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Child Activities"
        verbose_name_plural = "Child Activities"

    def __str__(self):
        return str(self.childID) + " | " + str(self.activityID)


class ChildDayActivity(models.Model):
    childActivityID = models.ForeignKey(ChildActivity, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    hrs = models.IntegerField(default=0)
    mins = models.IntegerField(default=0)
    date = models.DateField(default=now)

    class Meta:
        verbose_name = "Child Day Activities"
        verbose_name_plural = "Child Day Activities"

    def __str__(self):
        return str(self.points) + " | " + str(self.childActivityID)
