from rest_framework import serializers
from apps.utils.fields import FileBase64Field
from .models import (
    Company,
    CompanyFile,
    CompanyCertificateStatus,
    CompanyCertificateFile,
    CompanyCertificate,
)

from apps.address.serializers import (
    CountrySerializer,
    StateSerializer,
    CitySerializer,
    AddressTypeSerializer,
    NeighborhoodTypeSerializer,
)
from apps.client.serializers import (
        ClientSerializer,
        ClientNameSerializer,
)

class CompanyFileSerializer(serializers.ModelSerializer):
    file = FileBase64Field(
        required=True,
        represent_in_base64=True,
        allow_null=True,
        allow_empty_file=True
    )

    class Meta:
        model = CompanyFile
        fields = [
            'id',
            'file',
            'file_name',
            'document_name',
            'annotation',
            'date_emission',
            'date_validity',
            'link_certificates',
            'company',
        ]

class CompanyFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyFile
        fields = [
            'id',
            'file_name',
            'document_name',
            'annotation',
            'date_emission',
            'date_validity',
            'link_certificates',
            'company',
        ]

class CompanySerializer(serializers.ModelSerializer):
    country_set = CountrySerializer(source='country', read_only=True)
    state_set = StateSerializer(source='state', read_only=True)
    city_set = CitySerializer(source='city', read_only=True)
    address_type_set = AddressTypeSerializer(source='address_type', read_only=True)
    neighborhood_type_set = NeighborhoodTypeSerializer(source='neighborhood_type', read_only=True)
    file_set = CompanyFileDetailSerializer(source='company_file', read_only=True, many=True)

    class Meta:
        model = Company
        fields = [
            'id',
            'corporate_name',
            'name_fantasy',
            'cnpj',
            'ie',
            'im',
            'email',
            'phone_number',
            'address',
            'address_type',
            'address_type_set',
            'neighborhood',
            'neighborhood_type',
            'neighborhood_type_set',
            'complement',
            'number',
            'city',
            'city_set',
            'state',
            'state_set',
            'country',
            'country_set',
            'zip_code',
            'margin_min',
            'tax_aliquot',
            'fixed_cost',
            'file_set',
            'difference',
        ]

class CompanyListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = [
            'id',
            'corporate_name',
            'name_fantasy',        
            'cnpj',
            'ie',
            'phone_number',
            'margin_min',
            'tax_aliquot',
            'fixed_cost',
            'difference',
        ]

class CompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'corporate_name',
            'name_fantasy'
        ]

class CompanyBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'cnpj',
            'corporate_name',
            'name_fantasy',
            'tax_aliquot',
            'margin_min',
            'fixed_cost',
        ]

class CompanyCertificateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyCertificateStatus

        fields = [
            'id',
            'name',
            'color',
        ]

class CompanyCertificateFileSerializer(serializers.ModelSerializer):
    file = FileBase64Field(
        required=True,
        represent_in_base64=True,
        allow_null=True,
        allow_empty_file=True
    )

    class Meta:
        model = CompanyCertificateFile
        fields = [
            'id',
            'file',
            'file_name',
            'certificate',
        ]

class CompanyCertificateFileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyCertificateFile
        fields = [
            'id',
            'file_name',
            'certificate',
        ]

class CompanyCertificateSerializer(serializers.ModelSerializer):
    status_set = CompanyCertificateStatusSerializer(source='status',
                                                    read_only=True)

    files_set = CompanyCertificateFileDetailSerializer(source='certificate_files',
                                                       read_only=True,
                                                       many=True)
    
    client_set = ClientNameSerializer(source='client',
                                      read_only=True)

    class Meta:
        model = CompanyCertificate
        fields = [
            'id',
            'client',
            'client_set',
            'files_set',
            'annotation',
            'end_authentication',
            'status',
            'status_set',
            'company',
        ]