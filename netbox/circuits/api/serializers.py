from __future__ import unicode_literals

from rest_framework import serializers

from circuits.constants import CIRCUIT_STATUS_CHOICES
from circuits.models import Provider, Circuit, CircuitTermination, CircuitType
from dcim.api.serializers import NestedSiteSerializer, InterfaceSerializer
from extras.api.customfields import CustomFieldModelSerializer
from tenancy.api.serializers import NestedTenantSerializer
from utilities.api import ChoiceFieldSerializer, ValidatedModelSerializer, WritableNestedSerializer


#
# Providers
#

class ProviderSerializer(CustomFieldModelSerializer):

    class Meta:
        model = Provider
        fields = [
            'id', 'name', 'slug', 'asn', 'account', 'portal_url', 'noc_contact', 'admin_contact', 'comments',
            'custom_fields', 'created', 'last_updated',
        ]


class NestedProviderSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuits-api:provider-detail')

    class Meta:
        model = Provider
        fields = ['id', 'url', 'name', 'slug']


#
# Circuit types
#

class CircuitTypeSerializer(ValidatedModelSerializer):

    class Meta:
        model = CircuitType
        fields = ['id', 'name', 'slug']


class NestedCircuitTypeSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuits-api:circuittype-detail')

    class Meta:
        model = CircuitType
        fields = ['id', 'url', 'name', 'slug']


#
# Circuits
#

class CircuitSerializer(CustomFieldModelSerializer):
    provider = NestedProviderSerializer()
    status = ChoiceFieldSerializer(choices=CIRCUIT_STATUS_CHOICES, required=False)
    type = NestedCircuitTypeSerializer()
    tenant = NestedTenantSerializer(required=False, allow_null=True)

    class Meta:
        model = Circuit
        fields = [
            'id', 'cid', 'provider', 'type', 'status', 'tenant', 'install_date', 'commit_rate', 'description',
            'comments', 'custom_fields', 'created', 'last_updated',
        ]


class NestedCircuitSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='circuits-api:circuit-detail')

    class Meta:
        model = Circuit
        fields = ['id', 'url', 'cid']


#
# Circuit Terminations
#

class CircuitTerminationSerializer(ValidatedModelSerializer):
    circuit = NestedCircuitSerializer()
    site = NestedSiteSerializer()
    interface = InterfaceSerializer(required=False, allow_null=True)

    class Meta:
        model = CircuitTermination
        fields = [
            'id', 'circuit', 'term_side', 'site', 'interface', 'port_speed', 'upstream_speed', 'xconnect_id', 'pp_info',
        ]
