from rest_framework import serializers
from .models import CSVModel

class UploadSerializer(serializers.Serializer):
    csv_file = serializers.FileField()


class CSVImportSerializer(serializers.ModelSerializer):

    class Meta:
        model = CSVModel
        fields = "__all__"

