from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    markers = models.JSONField(default=list)
    def __str__(self):
        return self.name
