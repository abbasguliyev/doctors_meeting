from django.db import models
import datetime
from django.utils.translation import gettext_lazy as _

class StatusOption(models.TextChoices):
    ACTIVE = "Active", _("Active")
    INACTIVE = "Inactive", _("Inactive")
        
        
class DoctorsRequest(models.TextChoices):
    ACCEPTED = "Accepted", _("Accepted")
    WAITING = "Waiting", _("Waiting")
    REJECTED = "Rejected", _("Rejected")