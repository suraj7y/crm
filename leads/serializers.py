from django.db.models import Q
from rest_framework import serializers
from common.models import User
from contacts.models import Contact
from leads.models import Lead, Department
from opportunity.models import Opportunity
from accounts.models import Account


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = '__all__'
        exclude = ('password','profile_pic', 'last_login', 'is_superuser', 'is_staff','date_joined','groups','user_permissions' )


class LeadInfoSerializer(serializers.ModelSerializer):
    #contacts= serializers.ListField(default = [])

    class Meta:
        model = Lead
        fields = '__all__'
        #exclude = ('contacts',)


    def to_representation(self, instance):
        my_fields = {'title', 'first_name', 'last_name', 'email', 'phone', 'status', 'source'
                     ,'address_line', 'street', 'city', 'state', 'postcode', 'country'
                     , 'website', 'description', 'account_name', 'opportunity_amount', 'created_on', 'enquery_type'
                     , 'pre_bid_status', 'region','created_by', 'assigned_to', 'tags', 'contacts', 'department'}
        data = super().to_representation(instance)
        for field in my_fields:
            try:
                if not data[field]:
                    data[field] = ""
            except KeyError:
                pass
        return data


class DepartmentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class MixInfoSerialize(serializers.Serializer):
    departments = DepartmentInfoSerializer(many=True)
    user = UserInfoSerializer(many=True)


class OpportunityInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity
        fields = '__all__'

    def to_representation(self, instance):
        my_fields = {'name', 'stage', 'currency', 'amount', 'lead_source', 'probability', 'closed_on'
                     ,'description', 'created_on', 'account', 'closed_by', 'created_by', 'contacts'
                     , 'assigned_to', 'tags'}
        data = super().to_representation(instance)
        for field in my_fields:
            try:
                if not data[field]:
                    data[field] = ""
            except KeyError:
                pass
        return data


class AccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    def to_representation(self, instance):
        my_fields = {'industry', 'billing_state', 'name', 'email', 'phone', 'billing_address_line','billing_street'
                     ,'billing_city', 'billing_postcode', 'billing_country', 'website', 'description', 'created_on'
                     , 'status', 'contact_name', 'created_by', 'lead', 'tags', 'contacts'}
        data = super().to_representation(instance)
        for field in my_fields:
            try:
                if not data[field]:
                    data[field] = ""
            except KeyError:
                pass
        return data


class DashboardSerializer(serializers.Serializer):
    opportunity = OpportunityInfoSerializer(many=True)
    account = AccountInfoSerializer(many=True)
    opportunity_count = serializers.SerializerMethodField()
    lead_count = serializers.SerializerMethodField()
    account_count = serializers.SerializerMethodField()
    contact_count = serializers.SerializerMethodField()
    success = serializers.SerializerMethodField()

    def get_opportunity_count(self, obj):
        return Opportunity.objects.all().count()

    def get_lead_count(self, obj):
        return Lead.objects.filter(~Q(status='converted')).count()

    def get_account_count(self, obj):
        return Account.objects.all().count()

    def get_contact_count(self, obj):
        return Contact.objects.all().count()
    def get_success(self, obj):

        return True


class ContactInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'

    def to_representation(self, instance):
        my_fields = {'first_name', 'last_name', 'email', 'phone', 'description', 'address', 'created_by', 'assigned_to'}
        data = super().to_representation(instance)
        for field in my_fields:
            try:
                if not data[field]:
                    data[field] = ""
            except KeyError:
                pass
        return data


class AccountPageDataSerializer(serializers.Serializer):
    lead = LeadInfoSerializer(many=True)
    contact = ContactInfoSerializer(many=True)
    success = serializers.SerializerMethodField()

    def get_success(self, obj):
        return True