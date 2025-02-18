from rest_framework import serializers
from .models import Franchise, SondaStatus, ScanReport, NetworkLatency, ApplicationVersion

class FranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        fields = '__all__'  # Inclure tous les champs ou les spécifier explicitement

class SondaStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SondaStatus
        fields = '__all__'

class ScanReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanReport
        fields = '__all__'

class NetworkLatencySerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkLatency
        fields = '__all__'

class ApplicationVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationVersion
        fields = '__all__'
