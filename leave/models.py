from django.db import models
from viewflow.models import Process


class LeaveProcess(Process):
    reason = models.CharField(max_length=150)
    approved = models.BooleanField(default=False)
