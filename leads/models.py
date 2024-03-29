from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from common.models import User
from common.utils import (LEAD_STATUS, LEAD_SOURCE,
                          COUNTRIES, return_complete_address, DEPT_NAME, PRE_BID_STATUS,REGION)
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import Tags
from contacts.models import Contact


class Department(models.Model):
    code = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Lead(models.Model):
    title = models.CharField(
        pgettext_lazy("Treatment Pronouns for the customer",
                      "Title"), max_length=64)
    first_name = models.CharField(("First name"), null=True, max_length=255)
    last_name = models.CharField(("Last name"), null=True, max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    status = models.CharField(
        _("Status of Lead"),
        max_length=255, blank=True,
        null=True, choices=LEAD_STATUS)
    source = models.CharField(
        _("Source of Lead"), max_length=255,
        blank=True, null=True, choices=LEAD_SOURCE)
    address_line = models.CharField(
        _("Address"), max_length=255, blank=True, null=True)
    street = models.CharField(
        _("Street"), max_length=55, blank=True, null=True)
    city = models.CharField(_("City"), max_length=255, blank=True, null=True)
    state = models.CharField(_("State"), max_length=255, blank=True, null=True)
    postcode = models.CharField(
        _("Post/Zip-code"), max_length=64, blank=True, null=True)
    country = models.CharField(
        max_length=3, choices=COUNTRIES, blank=True, null=True)
    website = models.CharField(
        _("Website"), max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ManyToManyField(
        User, related_name='lead_assigned_users')
    account_name = models.CharField(max_length=255, null=True, blank=True)
    opportunity_amount = models.DecimalField(
        _("Opportunity Amount"),
        decimal_places=2, max_digits=12,
        blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name='lead_created_by',
        on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    is_active = models.BooleanField(default=False)
    enquery_type = models.CharField(max_length=255, blank=True, null=True)
    tags = models.ManyToManyField(Tags, blank=True)
    contacts = models.ManyToManyField(Contact, related_name="lead_contacts", blank=True)
    department =models.ManyToManyField(
        Department, related_name='department')
    pre_bid_status = models.CharField(
        _("pre_bid_status"), max_length=255,
        blank=True, null=True, choices=PRE_BID_STATUS)
    region = models.CharField(
        _("region"), max_length=255,
        blank=True, null=True, choices=REGION)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.first_name + self.last_name

    def get_complete_address(self):
        return return_complete_address(self)
